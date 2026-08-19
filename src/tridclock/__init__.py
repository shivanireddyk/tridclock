"""tridclock: TRID disclosure timing and fee tolerance, with the reasoning attached.

Two things mortgage lenders get wrong in software, both handled here:

1. Regulation Z uses TWO different definitions of "business day" for two
   different deadlines. Using the wrong one produces a date that looks
   plausible and is wrong.

2. Fee tolerance is not one rule. Zero-tolerance fees are tested individually,
   ten-percent fees cumulatively, and mixing the two produces a cure figure
   that is off in either direction.

Every result carries a plain-language explanation so a compliance analyst can
check the work without reading the source.
"""

from .calendars import BusinessCalendar, GeneralCalendar, PreciseCalendar
from .holidays import federal_holidays, is_federal_holiday
from .timing import (
    Deadline,
    DeliveryMethod,
    closing_disclosure_deadline,
    earliest_closing,
    earliest_consummation,
    loan_estimate_deadline,
    loan_estimate_waiting_period,
    presumed_receipt,
)
from .tolerance import Bucket, Fee, ToleranceResult, check_tolerance, reset_baseline

__version__ = "0.1.0"

__all__ = [
    "BusinessCalendar",
    "GeneralCalendar",
    "PreciseCalendar",
    "federal_holidays",
    "is_federal_holiday",
    "Deadline",
    "DeliveryMethod",
    "loan_estimate_deadline",
    "presumed_receipt",
    "earliest_consummation",
    "closing_disclosure_deadline",
    "loan_estimate_waiting_period",
    "earliest_closing",
    "Bucket",
    "Fee",
    "ToleranceResult",
    "check_tolerance",
    "reset_baseline",
]
