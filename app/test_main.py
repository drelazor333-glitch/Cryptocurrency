import pytest
from unittest.mock import patch
from app.main import cryptocurrency_action


class TestCryptocurrencyAction:
    """Tests for cryptocurrency_action function"""

    @patch('app.main.get_exchange_rate_prediction')
    def test_buy_when_rate_increases_more_than_5_percent(self, mock_prediction):
        """Should return 'Buy more cryptocurrency' when predicted rate is >5% higher"""
        current_rate = 100
        mock_prediction.return_value = 106  # 6% increase

        result = cryptocurrency_action(current_rate)

        assert result == "Buy more cryptocurrency"
        mock_prediction.assert_called_once()

    @patch('app.main.get_exchange_rate_prediction')
    def test_buy_at_exactly_5_percent_increase(self, mock_prediction):
        """Should return 'Buy more cryptocurrency' when predicted rate is exactly >5% higher"""
        current_rate = 100
        mock_prediction.return_value = 105.01  # Just over 5%

        result = cryptocurrency_action(current_rate)

        assert result == "Buy more cryptocurrency"

    @patch('app.main.get_exchange_rate_prediction')
    def test_do_nothing_at_5_percent_boundary_buy_side(self, mock_prediction):
        """Should return 'Do nothing' when predicted rate is exactly at 5% boundary"""
        current_rate = 100
        mock_prediction.return_value = 105  # Exactly 5%

        result = cryptocurrency_action(current_rate)

        assert result == "Do nothing"

    @patch('app.main.get_exchange_rate_prediction')
    def test_sell_when_rate_decreases_more_than_5_percent(self, mock_prediction):
        """Should return 'Sell all your cryptocurrency' when predicted rate is >5% lower"""
        current_rate = 100
        mock_prediction.return_value = 94  # 6% decrease

        result = cryptocurrency_action(current_rate)

        assert result == "Sell all your cryptocurrency"

    @patch('app.main.get_exchange_rate_prediction')
    def test_sell_at_exactly_5_percent_decrease(self, mock_prediction):
        """Should return 'Sell all your cryptocurrency' when predicted rate is exactly >5% lower"""
        current_rate = 100
        mock_prediction.return_value = 94.99  # Just over 5% decrease

        result = cryptocurrency_action(current_rate)

        assert result == "Sell all your cryptocurrency"

    @patch('app.main.get_exchange_rate_prediction')
    def test_do_nothing_at_5_percent_boundary_sell_side(self, mock_prediction):
        """Should return 'Do nothing' when predicted rate is exactly at -5% boundary"""
        current_rate = 100
        mock_prediction.return_value = 95  # Exactly 5% decrease

        result = cryptocurrency_action(current_rate)

        assert result == "Do nothing"

    @patch('app.main.get_exchange_rate_prediction')
    def test_do_nothing_when_no_significant_change(self, mock_prediction):
        """Should return 'Do nothing' when change is within ±5%"""
        current_rate = 100
        mock_prediction.return_value = 100  # No change

        result = cryptocurrency_action(current_rate)

        assert result == "Do nothing"

    @patch('app.main.get_exchange_rate_prediction')
    def test_do_nothing_with_small_positive_change(self, mock_prediction):
        """Should return 'Do nothing' for small positive changes"""
        current_rate = 100
        mock_prediction.return_value = 102  # 2% increase

        result = cryptocurrency_action(current_rate)

        assert result == "Do nothing"

    @patch('app.main.get_exchange_rate_prediction')
    def test_do_nothing_with_small_negative_change(self, mock_prediction):
        """Should return 'Do nothing' for small negative changes"""
        current_rate = 100
        mock_prediction.return_value = 98  # 2% decrease

        result = cryptocurrency_action(current_rate)

        assert result == "Do nothing"

    @patch('app.main.get_exchange_rate_prediction')
    def test_with_decimal_rates(self, mock_prediction):
        """Should work correctly with decimal rates"""
        current_rate = 50.25
        mock_prediction.return_value = 53.76  # ~6.98% increase

        result = cryptocurrency_action(current_rate)

        assert result == "Buy more cryptocurrency"