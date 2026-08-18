import httpx
import pytest

from mfcloud.errors import (
    APIErrorDetail,
    MFCAuthError,
    MFCloudError,
    MFCPermissionError,
    MFCRateLimitError,
    MFCServerError,
    MFCValidationError,
    parse_oauth_error_details,
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


def test_parse_oauth_error_details_rfc_body():
    details = parse_oauth_error_details(
        make_response(401, body={"error": "invalid_client", "error_description": "bad secret"})
    )
    assert len(details) == 1
    assert details[0].code == "invalid_client"
    assert details[0].message == "bad secret"


def test_parse_oauth_error_details_missing_description():
    details = parse_oauth_error_details(make_response(401, body={"error": "invalid_grant"}))
    assert details == [APIErrorDetail(code="invalid_grant", message="")]


def test_parse_oauth_error_details_api_shaped_body_is_ignored():
    assert parse_oauth_error_details(make_response(401)) == []  # {"errors": [...]} shape


def test_parse_oauth_error_details_non_json_body():
    response = httpx.Response(
        401, text="<html>", request=httpx.Request("POST", "https://api.test/token")
    )
    assert parse_oauth_error_details(response) == []


def test_all_errors_are_mfclouderror():
    for cls in (MFCValidationError, MFCAuthError, MFCRateLimitError, MFCServerError):
        assert issubclass(cls, MFCloudError)
