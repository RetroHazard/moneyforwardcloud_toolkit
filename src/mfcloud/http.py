"""Rate-limited, retrying HTTP transport.

The API allows 3 requests/second per (Client ID, office). We enforce it client-side by
spacing request *starts* at least 1/3 s apart (conservative pacing rather than a token
bucket — the API documents no burst allowance). Retry policy:

- 429: retry all methods (the request was rejected before processing, so retrying can't
  double-apply a write). Honors Retry-After when present, else exponential backoff.
- 5xx / transport errors: retried for GET only. Writes are NEVER auto-retried — an
  ambiguous journal-create timeout retried automatically could double-book real
  accounting data.

Clock/sleep/jitter are injectable so tests run instantly with a fake clock.
"""

from __future__ import annotations

import random
import threading
import time
from collections.abc import Callable

import httpx

BASE_URL = "https://api-accounting.moneyforward.com"
MIN_INTERVAL = 1 / 3
MAX_ATTEMPTS = 3
RETRYABLE_5XX = {500, 502, 503, 504}


class RateLimitedRetryTransport(httpx.BaseTransport):
    def __init__(
        self,
        inner: httpx.BaseTransport | None = None,
        *,
        min_interval: float = MIN_INTERVAL,
        max_attempts: int = MAX_ATTEMPTS,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        jitter: Callable[[], float] | None = None,
    ) -> None:
        self._inner = inner or httpx.HTTPTransport()
        self._min_interval = min_interval
        self._max_attempts = max_attempts
        self._clock = clock
        self._sleep = sleep
        self._jitter = jitter or (lambda: random.uniform(0, 0.5))
        self._lock = threading.Lock()
        self._next_start = 0.0

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            attempt += 1
            self._pace()
            try:
                response = self._inner.handle_request(request)
            except httpx.TransportError:
                if request.method != "GET" or attempt >= self._max_attempts:
                    raise
                self._sleep(self._backoff(attempt))
                continue

            if response.status_code == 429 and attempt < self._max_attempts:
                self._discard(response)
                self._sleep(self._retry_after(response) or self._backoff(attempt))
                continue
            if (
                response.status_code in RETRYABLE_5XX
                and request.method == "GET"
                and attempt < self._max_attempts
            ):
                self._discard(response)
                self._sleep(self._backoff(attempt))
                continue
            return response

    def close(self) -> None:
        self._inner.close()

    def _pace(self) -> None:
        with self._lock:
            now = self._clock()
            start = max(now, self._next_start)
            self._next_start = start + self._min_interval
        if start > now:
            self._sleep(start - now)

    def _backoff(self, attempt: int) -> float:
        return 2 ** (attempt - 1) + self._jitter()

    @staticmethod
    def _retry_after(response: httpx.Response) -> float | None:
        value = response.headers.get("Retry-After")
        try:
            return max(0.0, float(value)) if value is not None else None
        except ValueError:
            return None

    @staticmethod
    def _discard(response: httpx.Response) -> None:
        try:
            response.read()
        finally:
            response.close()
