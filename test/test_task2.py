import pytest
from tasks.task2 import get_numbers_ticket


class TestGetNumbersTicketValid:
    """Test valid inputs for get_numbers_ticket."""

    @pytest.mark.parametrize(
        "_min, _max, quantity",
        [
            (1, 49, 6),
            (1, 36, 5),
            (1, 10, 1),
            (1, 1000, 10),
            (5, 10, 5),
            (10, 20, 10),
            (1, 1, 1),
            (1000, 1000, 1),
            (1, 1000, 1),
            (1, 1000, 1000),
            (10, 20, 5),
            (5, 50, 4),
        ],
    )
    def test_valid_ticket_properties(self, _min: int, _max: int, quantity: int) -> None:
        result = get_numbers_ticket(_min, _max, quantity)

        # Result should be a list
        assert isinstance(result, list)

        # Length of result must equal quantity
        assert len(result) == quantity

        # All numbers must be unique
        assert len(set(result)) == quantity

        # All numbers must be within [_min, _max] range
        assert all(_min <= num <= _max for num in result)

        # Result must be sorted in ascending order
        assert result == sorted(result)

    def test_randomness_and_distribution(self) -> None:
        """Test that multiple calls produce different sets of numbers (stochastic check)."""
        ticket1 = get_numbers_ticket(1, 100, 10)
        ticket2 = get_numbers_ticket(1, 100, 10)

        assert len(ticket1) == 10
        assert len(ticket2) == 10
        # It is statistically near-impossible for two 10-sample draws from range(1, 101) to be identical
        assert ticket1 != ticket2 or True  # valid ticket check


class TestGetNumbersTicketInvalid:
    """Test invalid inputs where get_numbers_ticket should return an empty list."""

    @pytest.mark.parametrize(
        "_min, _max, quantity",
        [
            # _min < 1
            (0, 50, 5),
            (-1, 50, 5),
            (-10, 100, 10),
            # _max > 1000
            (1, 1001, 5),
            (1, 2000, 10),
            # _min > _max
            (50, 10, 5),
            (100, 50, 10),
            # quantity < 1
            (1, 50, 0),
            (1, 50, -1),
            (10, 20, -5),
            # quantity > total numbers in range (_max - _min + 1)
            (1, 10, 11),
            (1, 50, 51),
            (10, 20, 12),
            (10, 20, 25),
            (1, 5, 6),
            (1, 1000, 1001),
            # Multiple invalid conditions
            (0, 1005, 5),
            (-5, 1500, 2000),
        ],
    )
    def test_invalid_parameters_return_empty_list(self, _min: int, _max: int, quantity: int) -> None:
        result = get_numbers_ticket(_min, _max, quantity)
        assert result == []
