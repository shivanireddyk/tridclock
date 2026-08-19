"""US federal holidays as defined in 5 U.S.C. 6103(a).

Regulation Z's "precise" business day definition (12 CFR 1026.2(a)(6)) excludes
Sundays and "the legal public holidays specified in 5 U.S.C. 6103(a)". This
module computes those dates.

A deliberate design note, because it is the subtlest part of this file:

  5 U.S.C. 6103(a) names ELEVEN holidays by their actual date or rule (for
  example, "Christmas Day, December 25"). Separately, 6103(b) provides that
  when a holiday falls on a non-workday, federal employees observe it on an
  adjacent day.

  For TRID's precise business-day count, the regulation points at 6103(a),
  not 6103(b). So the strict reading is that only the ACTUAL date is excluded,
  and a Friday observance of a Saturday holiday is still a business day.

  This is a genuine ambiguity in the industry and lenders differ. Rather than
  silently pick one, `federal_holidays()` takes an `observed` flag so the
  caller makes the choice explicitly, and both behaviours are tested.
"""

from __future__ import annotations

from datetime import date, timedelta
from functools import lru_cache

__all__ = ["federal_holidays", "is_federal_holiday", "HOLIDAY_NAMES"]

HOLIDAY_NAMES = (
    "New Year's Day",
    "Birthday of Martin Luther King, Jr.",
    "Washington's Birthday",
    "Memorial Day",
    "Juneteenth National Independence Day",
    "Independence Day",
    "Labor Day",
    "Columbus Day",
    "Veterans Day",
    "Thanksgiving Day",
    "Christmas Day",
)


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """The nth occurrence of `weekday` in a month. weekday: Monday=0 .. Sunday=6."""
    d = date(year, month, 1)
    offset = (weekday - d.weekday()) % 7
    return d + timedelta(days=offset + 7 * (n - 1))


def _last_weekday(year: int, month: int, weekday: int) -> date:
    """The last occurrence of `weekday` in a month."""
    if month == 12:
        nxt = date(year + 1, 1, 1)
    else:
        nxt = date(year, month + 1, 1)
    last = nxt - timedelta(days=1)
    return last - timedelta(days=(last.weekday() - weekday) % 7)


def _observed(d: date) -> date:
    """5 U.S.C. 6103(b): Saturday holidays observed Friday, Sunday holidays Monday."""
    if d.weekday() == 5:  # Saturday
        return d - timedelta(days=1)
    if d.weekday() == 6:  # Sunday
        return d + timedelta(days=1)
    return d


@lru_cache(maxsize=256)
def federal_holidays(year: int, observed: bool = False) -> frozenset[date]:
    """Return the federal holidays for `year`.

    Args:
        year: calendar year.
        observed: if True, shift weekend holidays to their observed weekday per
            5 U.S.C. 6103(b). If False (the default, and the stricter reading
            for TRID) return the actual dates named in 6103(a).
    """
    actual = [
        date(year, 1, 1),                      # New Year's Day
        _nth_weekday(year, 1, 0, 3),           # MLK Jr., 3rd Monday in January
        _nth_weekday(year, 2, 0, 3),           # Washington's Birthday, 3rd Mon Feb
        _last_weekday(year, 5, 0),             # Memorial Day, last Monday in May
        date(year, 6, 19),                     # Juneteenth
        date(year, 7, 4),                      # Independence Day
        _nth_weekday(year, 9, 0, 1),           # Labor Day, 1st Monday in September
        _nth_weekday(year, 10, 0, 2),          # Columbus Day, 2nd Monday in October
        date(year, 11, 11),                    # Veterans Day
        _nth_weekday(year, 11, 3, 4),          # Thanksgiving, 4th Thursday in Nov
        date(year, 12, 25),                    # Christmas Day
    ]
    if observed:
        return frozenset(_observed(d) for d in actual)
    return frozenset(actual)


def is_federal_holiday(d: date, observed: bool = False) -> bool:
    """True if `d` is a federal holiday under the chosen reading."""
    return d in federal_holidays(d.year, observed)
