import pytest
import pandas as pd
from models.b76_model import B76OptionPricer

# Sample market data for testing
sample_market_data = pd.DataFrame({
    'DateAsOf': [20220101, 20220101],
    'FutureExpiryDate': [20230130, 20230130],
    'OptionType': ['Call', 'Put'],
    'StrikePrice': [50.0, 50.0],
    'CurrentPrice': [40, 40],
    'ImpliedVol': [0.15, 0.15]
})

# Expected option prices for the sample market data
expected_option_prices = [0.1068075255, 9.66089102470656]  # Replace with the correct expected prices

@pytest.fixture
def b76_option_pricer():
    return B76OptionPricer(sample_market_data)

def test_b76_option_pricer(b76_option_pricer):
    calculated_option_prices = b76_option_pricer.calculate_option_prices()
    assert len(calculated_option_prices) == len(sample_market_data)
    
    for index, row in calculated_option_prices.iterrows():
        assert row['OptionPrice'] == pytest.approx(expected_option_prices[index], abs=1e-6)
