import httpx
import pytest

from mfcloud.errors import (
    MFCAuthError,
    MFCloudError,
    MFCPermissionError,
    MFCRateLimitError,
    MFCServerError,
    MFCValidationError,
    raise_for_status,
)

ERROR_BODY = {"errors": [{"code": "invalid_query_parameter_value", "message": "bad page"}]}


def make_response(status: int, body=None) -> httpx.Response:
    return httpx.Response(
        status, json=body if body is not None else ERROR_BODY,
        request=httpx.Request("GET", "https://api.test/x"),
    )


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (400, MFCValidationError),
        (401, MFCAuthError),
        (403, MFCPermissionError),
        (409, MFCValidationError),
        (429, MFCRateLimitError),
        (500, MFCServerError),
        (503, MFCServerError),
    ],
)
def test_status_mapping(status, expected):
    with pytest.raises(expected) as excinfo:
        raise_for_status(make_response(status))
    assert excinfo.value.status == status
    assert excinfo.value.details[0].code == "invalid_query_parameter_value"
    assert "bad page" in str(excinfo.value)


def test_success_is_noop():
    raise_for_status(make_response(200, body={}))


def test_unparseable_body_still_raises_typed_error():
    response = httpx.Response(
        500, text="<html>oops</html>", request=httpx.Request("GET", "https://api.test/x")
    )
    with pytest.raises(MFCServerError) as excinfo:
        raise_for_status(response)
    assert excinfo.value.details == []
    assert "no error details" in str(excinfo.value)


def test_all_errors_are_mfclouderror():
    for cls in (MFCValidationError, MFCAuthError, MFCRateLimitError, MFCServerError):
        assert issubclass(cls, MFCloudError)
