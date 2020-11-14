from typing import Dict
from app.value.fundamentals import Fundamentals

from app.value.forecast import ForecastLR
from app.value.utils import Utils

from datetime import datetime

import pandas as pd
import numpy as np


class Ratios(Fundamentals):
    def __init__(self, data: Dict):
        super().__init__(data)
        self.df_historical_eps = self.__get_historical_eps()

    def get_wall_street_target_price(self):
        try:
            return round(self.df_highlights["WallStreetTargetPrice"].iloc[0], 2)
        except TypeError:
            return 0.0

    def get_price_book_mqr(self):
        try:
            return round(self.df_valuation["PriceBookMRQ"].iloc[0], 2)
        except TypeError:
            return 0.0

    def get_peg(self):
        try:
            return round(self.df_highlights["PEGRatio"].iloc[0], 2)
        except TypeError:
            return 0.0

    # Enterprise Value calculations

    def get_enterprise_value(self):
        # ev = round(float(self.get_marketcap() + self.get_total_debt() - self.get_cash()), 2)
        ev = round(self.get_ev_ebitda() * self.get_ebitda(), 2)
        return ev

    def __get_enterprise_value_historical(self):
        df_marketcap = self.get_marketcap_historical()[["year", "quarter", "marketcap"]]
        df_total_debt = self.get_total_debt_historical()[["year", "quarter", "total_debt"]]
        df_cash = self.get_cash_historical()[["year", "quarter", "cash"]]

        df_marketcap_total_debt = df_marketcap.merge(
            df_total_debt, left_index=True, right_index=True
        )

        df_enterprise_value = df_marketcap_total_debt.merge(
            df_cash, left_index=True, right_index=True
        )

        df_enterprise_value["enterprise_value"] = df_enterprise_value["marketcap"] + (
            df_enterprise_value["total_debt"] - df_enterprise_value["cash"]
        )

        return df_enterprise_value.replace(np.nan, 0)

    def get_enterprise_value_historical(self):
        ev = self.__get_enterprise_value_historical()[
            ["year", "quarter", "enterprise_value"]
        ].to_dict()
        return ev

    # The recommendation is not to forecast enterprise value. This methos is a candidate to be removed
    def get_enterprise_value_forecast(self):
        marketcap = self.get_marketcap()
        cash_dict = self.get_cash_forecast()
        total_debt_dict = self.get_total_debt_forecast()
        df_cash = pd.DataFrame(columns=["year", "quarter", "cash"])
        df_total_debt = pd.DataFrame(columns=["year", "quarter", "total_debt"])

        for cash in cash_dict:
            df_cash = df_cash.append(cash, ignore_index=True)

        for total_debt in total_debt_dict:
            df_total_debt = df_total_debt.append(total_debt, ignore_index=True)

        df_ev_forecast = df_cash.merge(df_total_debt, left_index=True, right_index=True)

        df_ev_forecast["enterprise_value"] = marketcap + (
            df_ev_forecast["total_debt"] - df_ev_forecast["cash"]
        )

        return df_ev_forecast

    # EV/EBITDA calculations
    def get_ev_ebitda(self):
        try:
            return round(self.df_valuation["EnterpriseValueEbitda"].iloc[0], 2)
        except TypeError:
            return 0.0

    def __get_ev_ebitda_forecast(self):
        ebitda_dict = self.get_ebitda_forecast()
        df_ebitda_forecast = pd.DataFrame(columns=["year", "quarter", "ebitda"])

        for ebitda in ebitda_dict:
            df_ebitda_forecast = df_ebitda_forecast.append(ebitda, ignore_index=True)

        df_ebitda_forecast["ev_ebitda"] = self.get_enterprise_value() / df_ebitda_forecast["ebitda"]

        return df_ebitda_forecast

    def get_ev_ebitda_forecast(self):
        return self.__get_ev_ebitda_forecast().to_dict()

    def get_price_ev_ebitda_forecast(self):
        future_ev_ebitda = self.__get_ev_ebitda_forecast()

        current_ev_ebitda = self.get_ev_ebitda()

        current_price = self.get_stock_price()

        future_ev_ebitda["ev_ebitda_price"] = (
            current_ev_ebitda * current_price
        ) / future_ev_ebitda["ev_ebitda"]

        print(future_ev_ebitda.head(10))

        return future_ev_ebitda

    # EV/EBIT calculations

    def __get_ev_ebit_forecast(self):
        ebit_dict = self.get_ebit_forecast()
        df_ebit_forecast = pd.DataFrame(columns=["year", "quarter", "ebit"])

        for ebit in ebit_dict:
            df_ebit_forecast = df_ebit_forecast.append(ebit, ignore_index=True)

        df_ev_ebit_forecast = df_ebit_forecast

        df_ev_ebit_forecast["ev_ebit"] = self.get_enterprise_value() / df_ev_ebit_forecast["ebit"]

        return df_ev_ebit_forecast

    def get_ev_ebit_forecast(self):
        return self.__get_ev_ebit_forecast().to_dict()

    def get_ev_ebit(self):
        return round(self.get_enterprise_value() / self.get_ebit_ttm(), 2)

    def get_price_ev_ebit_forecast(self):
        future_ev_ebit = self.__get_ev_ebit_forecast()

        current_ev_ebit = self.get_ev_ebit()

        current_price = self.get_stock_price()

        future_ev_ebit["ev_ebit_price"] = (current_ev_ebit * current_price) / future_ev_ebit[
            "ev_ebit"
        ]

        return future_ev_ebit

    # EV/FCF calculations

    def __get_ev_fcf_forecast(self):
        fcf_dict = self.get_fcf_forecast()
        df_fcf = pd.DataFrame(columns=["year", "quarter", "fcf"])

        for fcf in fcf_dict:
            df_fcf = df_fcf.append(fcf, ignore_index=True)

        df_fcf["ev_fcf"] = self.get_enterprise_value() / df_fcf["fcf"]

        return df_fcf

    def get_ev_fcf(self):
        return round(self.get_enterprise_value() / self.get_fcf(), 2)

    def get_price_ev_fcf_forecast(self):
        future_ev_fcf = self.__get_ev_fcf_forecast()

        current_ev_fcf = self.get_ev_fcf()

        current_price = self.get_stock_price()

        future_ev_fcf["ev_fcf_price"] = (current_ev_fcf * current_price) / future_ev_fcf["ev_fcf"]

        return future_ev_fcf

    # EPS calculations

    def get_eps_diluted_ttm(self):
        try:
            return round(self.df_highlights["DilutedEpsTTM"].iloc[0], 2)
        except TypeError:
            return 0.0

    def get_eps_ttm(self):
        eps, net_income, outstanding_shares = self.__get_current_eps()
        return round(eps, 2)

    def __get_current_eps(self):

        net_income_value = self.get_net_income_ttm()

        # getting outstanding shares dataframe
        if self.df_balance_sheet_quarterly.empty:
            eps = self.df_highlights["EarningsShare"].iloc[0]
            return eps, net_income_value, self.df_shares_stats["SharesOutstanding"].iloc[0]

        df_outstanding_shares = self.df_balance_sheet_quarterly[
            ["date", "commonStockSharesOutstanding"]
        ]
        df_outstanding_shares.sort_values("date", ascending=False, inplace=True)
        df_outstanding_shares = df_outstanding_shares.dropna()

        if df_outstanding_shares.empty:
            outstanding_shares_value = self.df_shares_stats["SharesOutstanding"].iloc[0]
        else:
            outstanding_shares_last_date_available = df_outstanding_shares["date"].max()
            outstanding_shares = df_outstanding_shares.loc[
                df_outstanding_shares["date"] == outstanding_shares_last_date_available
            ]
            outstanding_shares_value = outstanding_shares["commonStockSharesOutstanding"].iloc[0]

        try:
            eps = float(net_income_value) / float(outstanding_shares_value)
        except ZeroDivisionError:
            eps = self.df_highlights["EarningsShare"].iloc[0]

        return eps, net_income_value, outstanding_shares_value

    def __get_historical_eps(self):
        today = datetime.today().date()
        quarter_today = pd.Timestamp(today).quarter
        year_today = pd.Timestamp(today).year

        # getting net income TTM dataframe
        df_net_income_ttm = (
            self.df_income_statement_quarterly["netIncome"].rolling(4).sum().shift(-3)
        )
        df_net_income_ttm = df_net_income_ttm.dropna().to_frame()
        df_net_income_ttm = df_net_income_ttm.reset_index()
        df_net_income_ttm.rename(columns={"index": "date"}, inplace=True)

        if df_net_income_ttm.empty:
            df_net_income_ttm = (
                self.df_income_statement_quarterly["netIncomeApplicableToCommonShares"]
                .rolling(4)
                .sum()
                .shift(-3)
            )
            df_net_income_ttm = df_net_income_ttm.dropna().to_frame()
            df_net_income_ttm = df_net_income_ttm.reset_index()
            df_net_income_ttm.rename(columns={"index": "date"}, inplace=True)
            df_net_income_ttm.rename(
                columns={"netIncomeApplicableToCommonShares": "netIncome"}, inplace=True
            )

        if df_net_income_ttm.empty:
            eps_list = list()
            eps, max_net_income_value, shares = self.__get_current_eps()
            eps_dict = dict(
                {
                    "eps": eps,
                    "quarter": quarter_today,
                    "year": year_today,
                    "net_income": max_net_income_value,
                    "shares": shares,
                }
            )
            eps_list.append(eps_dict)
            df_eps = pd.DataFrame(eps_list)
            return df_eps

        df_net_income_ttm["date"] = pd.to_datetime(df_net_income_ttm["date"], format="%Y-%m-%d")
        df_net_income_ttm["quarter"] = df_net_income_ttm.apply(
            lambda x: pd.Timestamp(x["date"]).quarter, axis=1
        )
        df_net_income_ttm["year"] = df_net_income_ttm.apply(
            lambda x: pd.Timestamp(x["date"]).year, axis=1
        )

        net_income_last_date_available = df_net_income_ttm["date"].max()
        max_net_income_serie = df_net_income_ttm.loc[
            df_net_income_ttm["date"] == net_income_last_date_available
        ]
        max_net_income_quarter = max_net_income_serie["quarter"].iloc[0]
        max_net_income_year = max_net_income_serie["year"].iloc[0]

        # getting outstanding shares dataframe
        try:
            df_outstanding_shares = self.df_balance_sheet_quarterly[
                ["date", "commonStockSharesOutstanding"]
            ]
        except KeyError:
            eps_list = list()
            eps, max_net_income_value, shares = self.__get_current_eps()
            eps_dict = dict(
                {
                    "eps": eps,
                    "quarter": max_net_income_quarter,
                    "year": max_net_income_year,
                    "net_income": max_net_income_value,
                    "shares": shares,
                }
            )
            eps_list.append(eps_dict)
            df_eps = pd.DataFrame(eps_list)
            return df_eps
        df_outstanding_shares.sort_values("date", ascending=False, inplace=True)

        df_outstanding_shares = df_outstanding_shares.dropna()

        if df_outstanding_shares.empty:
            eps_list = list()
            eps, max_net_income_value, shares = self.__get_current_eps()
            eps_dict = dict(
                {
                    "eps": eps,
                    "quarter": max_net_income_quarter,
                    "year": max_net_income_year,
                    "net_income": max_net_income_value,
                    "shares": shares,
                }
            )
            eps_list.append(eps_dict)
            df_eps = pd.DataFrame(eps_list)
            return df_eps
        else:
            df_outstanding_shares["date"] = pd.to_datetime(
                df_outstanding_shares["date"], format="%Y-%m-%d"
            )
            df_outstanding_shares["quarter"] = df_outstanding_shares.apply(
                lambda x: pd.Timestamp(x["date"]).quarter, axis=1
            )
            df_outstanding_shares["year"] = df_outstanding_shares.apply(
                lambda x: pd.Timestamp(x["date"]).year, axis=1
            )

            outstanding_shares_last_date_available = df_outstanding_shares["date"].max()
            max_outstanding_shares_serie = df_outstanding_shares.loc[
                df_outstanding_shares["date"] == outstanding_shares_last_date_available
            ]
            max_outstanding_shares_quarter = max_outstanding_shares_serie["quarter"].iloc[0]
            max_outstanding_shares_year = max_outstanding_shares_serie["year"].iloc[0]

            five_years_limit = max_net_income_serie["year"].iloc[0] - 5

            eps_list = list()

            eps, net_income, shares = self.__get_current_eps()

            max_net_income_value = max_net_income_serie["netIncome"].iloc[0]
            max_outstanding_shares_value = max_outstanding_shares_serie[
                "commonStockSharesOutstanding"
            ].iloc[0]
            eps_dict = dict(
                {
                    "eps": eps,
                    "quarter": max_net_income_quarter,
                    "year": max_net_income_year,
                    "net_income": max_net_income_value,
                    "shares": max_outstanding_shares_value,
                }
            )

            eps_list.append(eps_dict)

            while year_today > five_years_limit:

                if df_outstanding_shares.empty:
                    break

                outstanding_shares_serie = df_outstanding_shares.loc[
                    (df_outstanding_shares["quarter"] == max_outstanding_shares_quarter)
                    & (df_outstanding_shares["year"] == max_outstanding_shares_year)
                ]

                if outstanding_shares_serie.empty:
                    break

                outstanding_shares_value = outstanding_shares_serie[
                    "commonStockSharesOutstanding"
                ].iloc[0]

                if float(outstanding_shares_value) == 0.0:
                    break

                net_income_serie = df_net_income_ttm.loc[
                    (df_net_income_ttm["quarter"] == max_outstanding_shares_quarter)
                    & (df_net_income_ttm["year"] == max_outstanding_shares_year)
                ]

                if net_income_serie.empty:
                    break

                previous_net_income_value = net_income_serie["netIncome"].iloc[0]

                if float(previous_net_income_value) == 0.0:
                    break

                eps = float(previous_net_income_value) / float(outstanding_shares_value)
                eps_dict = dict(
                    {
                        "eps": eps,
                        "quarter": max_outstanding_shares_quarter,
                        "year": max_outstanding_shares_year,
                        "net_income": previous_net_income_value,
                        "shares": outstanding_shares_value,
                    }
                )
                eps_list.append((eps_dict))

                (
                    previous_quarter_outstanding_shares,
                    previous_year_outstanding_shares,
                ) = Utils.get_previous_quarter(
                    max_outstanding_shares_quarter, max_outstanding_shares_year
                )

                max_outstanding_shares_quarter = previous_quarter_outstanding_shares
                max_outstanding_shares_year = previous_year_outstanding_shares

                year_today = max_outstanding_shares_year

            df_eps = pd.DataFrame(eps_list)
            return df_eps

    def get_eps_historical(self):
        df_eps = self.__get_historical_eps()
        df_eps.drop_duplicates(keep="first", inplace=True)
        df_just_eps = df_eps[["quarter", "year", "eps"]]

        quarter, year = int(df_just_eps["quarter"].iloc[0]), int(df_just_eps["year"].iloc[0])

        eps_dict = dict(
            {"year": year, "quarter": quarter, "eps": float(round(df_just_eps["eps"].iloc[0], 2)),}
        )

        eps_list = list()

        eps_list.append(eps_dict)
        for j in range(1, df_eps.__len__()):
            quarter, year = Utils.get_next_quarter(quarter, year)
            eps_dict = dict(
                {
                    "year": int(df_just_eps["year"].iloc[j]),
                    "quarter": int(df_just_eps["quarter"].iloc[j]),
                    "eps": float(round(df_just_eps["eps"].iloc[j], 2)),
                }
            )
            eps_list.append(eps_dict)

        return eps_list

    def get_eps_forecast(self):
        df_eps = self.__get_historical_eps()
        df_eps.reset_index(inplace=True)
        x = df_eps["index"].to_numpy()
        y = df_eps["eps"].to_numpy()

        y_future = ForecastLR.get_forecast(x, y)

        quarter, year = int(df_eps["quarter"].iloc[0]), int(df_eps["year"].iloc[0])

        forecasting_dict = dict(
            {"year": year, "quarter": quarter, "eps": float(round(df_eps["eps"].iloc[0], 2)),}
        )

        forecast_list = list()

        forecast_list.append(forecasting_dict)
        for j in range(0, y_future.size):
            quarter, year = Utils.get_next_quarter(quarter, year)
            forecasting_dict = dict(
                {"year": year, "quarter": quarter, "eps": float(round(y_future[j][0], 2)),}
            )
            forecast_list.append(forecasting_dict)

        return forecast_list

    # PER calculations

    def get_per_ttm(self):
        try:
            return round(self.df_valuation["TrailingPE"].iloc[0], 2)
        except TypeError:
            return 0.0

    def get_per_forward(self):
        try:
            return round(self.df_valuation["ForwardPE"].iloc[0], 2)
        except TypeError:
            return 0.0

    def __get_per(self, stock_serie):
        quarter, year = Utils.get_previous_quarter(stock_serie["quarter"], stock_serie["year"])
        df = self.df_historical_eps
        df = df.loc[(df["quarter"] == quarter) & (df["year"] == year)]
        try:
            return float(stock_serie["close"]) / float(df["eps"].values[0])
        except (IndexError, TypeError, ZeroDivisionError) as e:
            return self.df_highlights["PERatio"].iloc[0]

    def get_current_per(self):
        # getting stocks dataframe
        df_stocks_close = self.df_stocks[["date", "close"]]
        df_stocks_close.sort_values("date", ascending=False, inplace=True)

        last_date_price_available = df_stocks_close["date"].max()
        stock_price_serie = df_stocks_close.loc[
            df_stocks_close["date"] == last_date_price_available
        ]
        stock_price_value = stock_price_serie["close"].iloc[0]
        eps, net_income, shares = self.__get_current_eps()
        per = stock_price_value / eps

        return per

    def get_historical_per(self):
        # getting stocks dataframe
        if self.df_stocks.empty:
            today = datetime.today().date()
            today_str = today.strftime("%Y-%m-%d")
            return {"per": self.df_highlights["PERatio"].iloc[0], "date": today_str}
        df_stocks_close_w_per = self.df_stocks[["date", "close"]]
        df_stocks_close_w_per.sort_values("date", ascending=False, inplace=True)

        df_stocks_close_w_per["date"] = df_stocks_close_w_per.apply(
            lambda x: pd.Timestamp(x["date"]), axis=1
        )
        df_stocks_close_w_per["quarter"] = df_stocks_close_w_per.apply(
            lambda x: pd.Timestamp(x["date"]).quarter, axis=1
        )
        df_stocks_close_w_per["year"] = df_stocks_close_w_per.apply(
            lambda x: pd.Timestamp(x["date"]).year, axis=1
        )

        df_stocks_close_w_per["per"] = df_stocks_close_w_per.apply(
            lambda x: self.__get_per(x), axis=1
        )

        just_per = df_stocks_close_w_per[["date", "per"]]
        just_per.dropna(inplace=True)
        if just_per.empty:
            today = datetime.today().date()
            today_str = today.strftime("%Y-%m-%d")
            return {"per": self.df_highlights["PERatio"].iloc[0], "date": today_str}
        just_per["per"] = round(just_per["per"], 2)
        just_per["date"] = just_per["date"].dt.strftime("%Y-%m-%d")
        just_per.set_index("date", inplace=True)
        per_dict = just_per.to_dict()

        return per_dict
