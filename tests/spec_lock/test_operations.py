"""Spec-lock: the client must cover the spec's operations, and models must match the
spec's schemas field-for-field. Parsed from spec/openapi.en.yaml — the source of truth."""

from pathlib import Path

import httpx
import yaml

from mfcloud.client import MFClient
from mfcloud.models import MODEL_FOR_SCHEMA, REQUEST_MODEL_FOR_SCHEMA
from mfcloud.resources.base import Resource

SPEC = yaml.safe_load(
    (Path(__file__).resolve().parent.parent.parent / "spec" / "openapi.en.yaml")
    .read_text(encoding="utf-8")
)


def spec_operation_ids() -> set[str]:
    return {
        op["operationId"]
        for methods in SPEC["paths"].values()
        for method, op in methods.items()
        if method in {"get", "post", "put", "delete"}
    }


def implemented_operation_ids() -> set[str]:
    client = MFClient(transport=httpx.MockTransport(lambda r: httpx.Response(500)))
    ids = set()
    for attr in vars(client).values():
        if isinstance(attr, Resource):
            for name in dir(attr):
                op_id = getattr(getattr(attr, name), "__operation_id__", None)
                if op_id:
                    ids.add(op_id)
    return ids


def test_operation_coverage_is_complete():
    """Every one of the spec's 23 operations has exactly one tagged client method."""
    expected = spec_operation_ids()
    implemented = implemented_operation_ids()
    assert len(expected) == 23
    missing = expected - implemented
    phantom = implemented - expected
    assert not missing, f"spec operations without client methods: {sorted(missing)}"
    assert not phantom, f"client methods claiming nonexistent operations: {sorted(phantom)}"


def _assert_field_parity(mapping) -> list[str]:
    schemas = SPEC["components"]["schemas"]
    problems = []
    for schema_name, model in mapping.items():
        spec_fields = set(schemas[schema_name].get("properties", {}))
        spec_fields.discard("XMLName")  # codegen artifact in error schemas, not real data
        model_fields = set(model.model_fields)
        if spec_fields != model_fields:
            problems.append(
                f"{schema_name}: missing={sorted(spec_fields - model_fields)}"
                f" extra={sorted(model_fields - spec_fields)}"
            )
    return problems


def test_response_model_fields_match_spec_schemas():
    problems = _assert_field_parity(MODEL_FOR_SCHEMA)
    assert not problems, "model/schema field drift:\n" + "\n".join(problems)


def test_request_model_fields_match_spec_schemas():
    problems = _assert_field_parity(REQUEST_MODEL_FOR_SCHEMA)
    assert not problems, "request model/schema field drift:\n" + "\n".join(problems)


def test_required_spec_fields_are_required_on_models():
    """Every spec-required field must not have a default (so validation catches gaps)."""
    schemas = SPEC["components"]["schemas"]
    problems = []
    for schema_name, model in MODEL_FOR_SCHEMA.items():
        required = set(schemas[schema_name].get("required", []))
        for field_name in required:
            info = model.model_fields.get(field_name)
            if info is not None and not info.is_required():
                problems.append(f"{schema_name}.{field_name} should be required")
    assert not problems, "\n".join(problems)
