from cpmonitor.models import ExecutionStatus
from cpmonitor.views import _sort_status_proportions

SOME_NUMBER = 20


def test_status_proportions_should_have_the_right_sorting_order_when_all_statuses_are_present():
    # given
    status_proportions = {
        ExecutionStatus.COMPLETE: SOME_NUMBER,
        ExecutionStatus.FAILED: SOME_NUMBER,
        ExecutionStatus.UNKNOWN: SOME_NUMBER,
        ExecutionStatus.AS_PLANNED: SOME_NUMBER,
        ExecutionStatus.DELAYED: SOME_NUMBER,
    }
    status_order = [
        ExecutionStatus.FAILED,
        ExecutionStatus.DELAYED,
        ExecutionStatus.AS_PLANNED,
        ExecutionStatus.COMPLETE,
        ExecutionStatus.UNKNOWN,
    ]
    expected_sorted_status_proportions = [
        (SOME_NUMBER, ExecutionStatus.FAILED),
        (SOME_NUMBER, ExecutionStatus.DELAYED),
        (SOME_NUMBER, ExecutionStatus.AS_PLANNED),
        (SOME_NUMBER, ExecutionStatus.COMPLETE),
        (SOME_NUMBER, ExecutionStatus.UNKNOWN),
    ]

    # when
    actual_sorted_status_proportions = _sort_status_proportions(
        status_proportions, status_order
    )

    # then
    assert expected_sorted_status_proportions == actual_sorted_status_proportions


def test_status_proportions_should_have_the_right_sorting_order_when_not_all_statuses_are_present():
    # given
    status_proportions = {
        ExecutionStatus.COMPLETE: SOME_NUMBER,
        ExecutionStatus.AS_PLANNED: SOME_NUMBER,
        ExecutionStatus.FAILED: SOME_NUMBER,
    }
    status_order = [
        ExecutionStatus.FAILED,
        ExecutionStatus.DELAYED,
        ExecutionStatus.AS_PLANNED,
        ExecutionStatus.COMPLETE,
        ExecutionStatus.UNKNOWN,
    ]
    expected_sorted_status_proportions = [
        (SOME_NUMBER, ExecutionStatus.FAILED),
        (SOME_NUMBER, ExecutionStatus.AS_PLANNED),
        (SOME_NUMBER, ExecutionStatus.COMPLETE),
    ]

    # when
    actual_sorted_status_proportions = _sort_status_proportions(
        status_proportions, status_order
    )

    # then
    assert expected_sorted_status_proportions == actual_sorted_status_proportions
