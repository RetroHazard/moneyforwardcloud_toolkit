"""Pydantic models mirroring the API's component schemas.

MODEL_FOR_SCHEMA maps spec schema names to model classes; the spec-lock tests use it
to assert field-level parity with spec/openapi.en.yaml.
"""

from mfcloud.models.accounts import Account, SubAccount
from mfcloud.models.common import Metadata, MFModel
from mfcloud.models.journals import (
    CRUDJournalResponse,
    GetJournalsResponse,
    JournalItem,
    JournalLine,
    JournalLineDetails,
)
from mfcloud.models.masters import (
    ConnectedAccount,
    ConnectedSubAccount,
    Department,
    Tax,
    TermSetting,
    TradePartner,
)
from mfcloud.models.office import AccountingPeriod, Office
from mfcloud.models.reports import TBResponse, TBRow, TransitionResponse, TransitionRow
from mfcloud.models.requests import REQUEST_MODEL_FOR_SCHEMA
from mfcloud.models.transactions import (
    CreatedTransaction,
    GetTransactionsResponse,
    Transaction,
)

MODEL_FOR_SCHEMA: dict[str, type[MFModel]] = {
    "Account": Account,
    "SubAccount": SubAccount,
    "Office": Office,
    "AccountingPeriod": AccountingPeriod,
    "Metadata": Metadata,
    "JournalItem": JournalItem,
    "JournalLine": JournalLine,
    "JournalLineDetails": JournalLineDetails,
    "GetJournalsResponse": GetJournalsResponse,
    "CRUDJournalResponse": CRUDJournalResponse,
    "Department": Department,
    "Tax": Tax,
    "TermSetting": TermSetting,
    "TradePartnersResponse_trade_partners_inner": TradePartner,
    "ConnectedAccount": ConnectedAccount,
    "ConnectedSubAccount": ConnectedSubAccount,
    "Transaction": Transaction,
    "GetTransactionsResponse": GetTransactionsResponse,
    "TBResponse": TBResponse,
    "TBRow": TBRow,
    "TransitionResponse": TransitionResponse,
    "TransitionRow": TransitionRow,
    "PostTransactionsResponse_transactions_inner": CreatedTransaction,
}

__all__ = [
    "MODEL_FOR_SCHEMA",
    "REQUEST_MODEL_FOR_SCHEMA",
    *sorted(cls.__name__ for cls in set(MODEL_FOR_SCHEMA.values())),
]
