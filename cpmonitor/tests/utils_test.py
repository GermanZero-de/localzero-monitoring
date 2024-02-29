from datetime import date
from freezegun import freeze_time
from cpmonitor.utils import RemainingTimeInfo


@freeze_time("2025-01-02")
def test_given_days_in_year_left_exceed_half_a_year_then_remaining_time_is_calculated_correctly():
    one_full_year_remaining = RemainingTimeInfo(date(2025, 1, 2), 2025)
    assert one_full_year_remaining.years_left == 0
    assert one_full_year_remaining.days_in_year_left == 364


@freeze_time("2025-01-01")
def test_given_days_in_year_left_is_exactly_a_year_then_remaining_time_is_calculated_correctly():
    one_full_year_remaining = RemainingTimeInfo(date(2025, 1, 1), 2025)
    assert one_full_year_remaining.years_left == 1
    assert one_full_year_remaining.days_in_year_left == 0


@freeze_time("2025-12-31")
def test_given_days_in_year_left_is_single_day_then_remaining_time_is_calculated_correctly():
    one_full_year_remaining = RemainingTimeInfo(date(2025, 12, 31), 2025)
    assert one_full_year_remaining.years_left == 0
    assert one_full_year_remaining.days_in_year_left == 1
