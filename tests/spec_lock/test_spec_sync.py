"""The English spec must mirror the Japanese spec structurally, byte-for-byte at the
data level, differing only in description/summary/title text."""

import re
from pathlib import Path

import yaml

from fetch_spec import diff_pointers
from translate_spec import JAPANESE_RE, TEXT_KEYS, strip_text, walk

SPEC_DIR = Path(__file__).resolve().parent.parent.parent / "spec"

EXPECTED_OPERATION_IDS = {
    "getAccounts", "getConnectedAccounts", "currentOffice",
    "getJournals", "postJournals", "getJournalById", "putJournals", "deleteJournals",
    "postVouchers", "deleteVouchers",
    "getTransactions", "postTransactions", "postTransactionJournalize",
    "getDepartments", "getTaxes", "getSubAccounts",
    "getReportsTrialBalanceBalanceSheet", "getReportsTrialBalanceProfitLoss",
    "getReportsTransitionBalanceSheet", "getReportsTransitionProfitLoss",
    "getTradePartners", "postTradePartners", "getTermSettings",
}


def load(name):
    return yaml.safe_load((SPEC_DIR / name).read_text(encoding="utf-8"))


def test_structural_identity():
    drift = diff_pointers(strip_text(load("openapi.ja.yaml")), strip_text(load("openapi.en.yaml")))
    assert not drift, f"ja/en structural mismatch at: {drift[:10]}"


def test_english_spec_has_no_japanese_text():
    # Japanese may remain only as quoted UI/setting literals (「税込」-style) or short
    # parenthesized glosses; free-running Japanese prose means a missed translation.
    literal_spans = re.compile(r"「[^」]*」|（[^）]*）|\([^)]*\)")
    found: dict[str, str] = {}
    walk(load("openapi.en.yaml"), "", found)
    untranslated = {
        pointer: text
        for pointer, text in found.items()
        if JAPANESE_RE.search(literal_spans.sub("", text))
    }
    assert not untranslated, f"untranslated Japanese remains at: {list(untranslated)[:10]}"


def test_all_operations_present():
    spec = load("openapi.en.yaml")
    ids = {
        op["operationId"]
        for methods in spec["paths"].values()
        for method, op in methods.items()
        if method in {"get", "post", "put", "delete"}
    }
    assert ids == EXPECTED_OPERATION_IDS


def test_reference_docs_cover_all_operations():
    docs = Path(__file__).resolve().parent.parent.parent / "docs" / "api"
    text = "".join(p.read_text(encoding="utf-8") for p in docs.glob("*.md"))
    for op_id in EXPECTED_OPERATION_IDS:
        assert f"`{op_id}`" in text, f"{op_id} missing from generated reference"


def test_text_keys_and_japanese_regex_sane():
    # Guard the extraction contract the pipeline relies on.
    assert {"description", "summary", "title"} == TEXT_KEYS
    assert JAPANESE_RE.search("勘定科目")
    assert not JAPANESE_RE.search("plain english only")
