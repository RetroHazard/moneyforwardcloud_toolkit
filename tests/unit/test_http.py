"""Rate limiter and retry policy tests — all against a fake clock, no real sleeping."""

import httpx
import pytest

from mfcloud.http import RateLimitedRetryTransport


class FakeTime:
    def __init__(self):
        self.now = 1000.0
        self.sleeps: list[float] = []

    def clock(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def make_transport(handler, fake: FakeTime, **kwargs) -> httpx.Client:
    transport = RateLimitedRetryTransport(
        inner=httpx.MockTransport(handler),
        clock=fake.clock,
        sleep=fake.sleep,
        jitter=lambda: 0.0,
        **kwargs,
    )
    return httpx.Client(transport=transport, base_url="https://api.test")


def test_paces_requests_to_min_interval():
    fake = FakeTime()
    client = make_transport(lambda request: httpx.Response(200), fake)
    for _ in range(4):
        client.get("/x")
    # First request goes immediately; each subsequent one waits 1/3 s after the last start.
    assert fake.sleeps == pytest.approx([1 / 3, 1 / 3, 1 / 3])


def test_no_pacing_delay_when_requests_are_naturally_spaced():
    fake = FakeTime()
    client = make_transport(lambda request: httpx.Response(200), fake)
    client.get("/x")
    fake.now += 10
    client.get("/x")
    assert fake.sleeps == []


def test_429_retried_with_backoff_then_succeeds():
    fake = FakeTime()
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(429) if len(calls) < 3 else httpx.Response(200)

    client = make_transport(handler, fake)
    response = client.get("/x")
    assert response.status_code == 200
    assert len(calls) == 3
    # Sleeps include pacing (1/3) and backoff (1, then 2).
    assert 1.0 in fake.sleeps and 2.0 in fake.sleeps


def test_429_exhausts_attempts_and_returns_response():
    fake = FakeTime()
    client = make_transport(lambda request: httpx.Response(429), fake)
    assert client.get("/x").status_code == 429


def test_429_retried_even_for_post():
    fake = FakeTime()
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(429) if len(calls) == 1 else httpx.Response(201)

    client = make_transport(handler, fake)
    assert client.post("/x", json={}).status_code == 201
    assert len(calls) == 2


def test_429_honors_retry_after_header():
    fake = FakeTime()
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(429, headers={"Retry-After": "7"})
        return httpx.Response(200)

    client = make_transport(handler, fake)
    assert client.get("/x").status_code == 200
    assert 7.0 in fake.sleeps


def test_5xx_retried_for_get():
    fake = FakeTime()
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(503) if len(calls) == 1 else httpx.Response(200)

    client = make_transport(handler, fake)
    assert client.get("/x").status_code == 200
    assert len(calls) == 2


def test_5xx_never_retried_for_write_methods():
    fake = FakeTime()
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(500)

    client = make_transport(handler, fake)
    for method in ("POST", "PUT", "DELETE"):
        calls.clear()
        response = client.request(method, "/x")
        assert response.status_code == 500
        assert len(calls) == 1, f"{method} must not be retried"


def test_transport_error_retried_for_get_only():
    fake = FakeTime()
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            raise httpx.ConnectError("boom")
        return httpx.Response(200)

    client = make_transport(handler, fake)
    assert client.get("/x").status_code == 200

    calls.clear()
    with pytest.raises(httpx.ConnectError):
        client.post("/x")
    assert len(calls) == 1
