from datetime import date
from freezegun import freeze_time
from cpmonitor.utils import RemainingTimeInfo


@freeze_time("2025-01-01")
def test_given_days_in_year_left_exceed_half_a_year_then_remaining_time_is_calculated_correctly():
    remaining = RemainingTimeInfo(date(2025, 1, 1), 2025)
    assert remaining.years_left == 0
    assert remaining.days_in_year_left == 365
