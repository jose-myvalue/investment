from typing import Dict
from app.value.fundamentals import Fundamentals


class Returns(Fundamentals):
    def __init__(self, data: Dict):
        super().__init__(data)

    def get_roe_ttm(self):
        try:
            return round(self.df_highlights["ReturnOnEquityTTM"].iloc[0] * 100, 2)
        except TypeError:
            return 0.0

    def get_roa_ttm(self):
        try:
            return round(self.df_highlights["ReturnOnAssetsTTM"].iloc[0] * 100, 2)
        except TypeError:
            return 0.0

    def get_roic_ttm(self):
        invested_capital = self.get_equity() + self.get_total_debt() - self.get_cash()
        return round((self.get_ebit_ttm() / invested_capital) * 100, 2)
