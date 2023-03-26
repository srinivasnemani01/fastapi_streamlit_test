import pandas as pd
import numpy as np
import scipy.stats as stats
from models.generic_option_pricer import IOptionPricer

RISK_FREE_RATE = 0.05

class B76OptionPricer(IOptionPricer):
    def __init__(self, market_data):
        super().__init__(market_data=market_data)

    def calculate_option_prices(self):
        option_prices = self.market_data
        option_prices['OptionPrice'] = option_prices.apply(self._black_76_option_price, axis=1)
        return option_prices

    def _black_76_option_price(self, row):
        F = row['CurrentPrice'] 
        K = row['StrikePrice']  
        sigma = row['ImpliedVol'] 

        date_as_of = pd.to_datetime(row['DateAsOf'], format='%Y%m%d')
        future_expiry_date = pd.to_datetime(row['FutureExpiryDate'], format='%Y%m%d')
        # 2 months before expiry as mentioned in the assignment document.
        settlement_date = future_expiry_date - pd.DateOffset(months=2)  
        T = (settlement_date - date_as_of).days / 365  # time to maturity in years

        r = RISK_FREE_RATE  # risk-free interest rate (Hard coded to  5% at the top of the file)

        d1 = (np.log(F / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        call_price = np.exp(-r * T) * (F * stats.norm.cdf(d1) - K * stats.norm.cdf(d2))
        put_price = np.exp(-r * T) * (K * stats.norm.cdf(-d2) - F * stats.norm.cdf(-d1))

        return call_price if row['OptionType'] == 'Call' else put_price
