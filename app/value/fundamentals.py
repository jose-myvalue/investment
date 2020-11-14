from datetime import datetime
from typing import Dict

from app.value.forecast import ForecastLR
from app.value.utils import Utils

import pandas as pd
import numpy as np

pd.options.display.float_format = "{:.2f}".format
pd.options.mode.chained_assignment = None

np.set_printoptions(suppress=True, formatter={"float_kind": "{:f}".format}, precision=2)


class Fundamentals:
    df_income_statement_quarterly = []
    df_balance_sheet_quarterly = []
    df_highlights = []

    df_income_statement_yearly = []
    df_balance_sheet_yearly = []

    df_stocks = []
    df_shares_stats = []
    df_historical_eps = []
    df_historical_net_income = []

    def __init__(self, data: Dict):

        self.ticker = data["General"]["Code"]

        self.df_highlights = pd.DataFrame(data["highlights"], index=[0])

        self.df_valuation = pd.DataFrame(data["valuation"], index=[0])

        self.df_income_statement_quarterly = pd.DataFrame(data["quarters_income_statement"]).T
        self.df_balance_sheet_quarterly = pd.DataFrame(data["quarters_balance_sheet"]).T
        self.df_cash_flow_quarterly = pd.DataFrame(data["quarters_cash_flow"]).T

        self.df_income_statement_yearly = pd.DataFrame(data["yearly_income_statement"]).T
        self.df_balance_sheet_yearly = pd.DataFrame(data["yearly_balance_sheet"]).T

        self.df_stocks = pd.DataFrame(data["Stocks"]).T

        self.df_shares_stats = pd.DataFrame(data["shares_stats"], index=[0])
        self.df_outstanding_shares_annual = pd.DataFrame(data["outstanding-shares-annual"]).T
        self.df_outstanding_shares_quarterly = pd.DataFrame(data["outstanding-shares-quarterly"]).T

        # self.df_balance_sheet_quarterly.reset_index(inplace=True)
        # self.df_stocks.reset_index(inplace=True)

    # STOCK PRICE
    def get_stock_price(self):
        try:
            df_stocks_flipped = self.df_stocks["close"].iloc[::-1]
            return round(df_stocks_flipped.iloc[0], 2)
        except TypeError:
            return 0.0

    def get_historical_stock_price(self):
        df_stocks_flipped = self.df_stocks["close"].iloc[::-1].to_frame()
        df_stocks_flipped.reset_index(inplace=True)
        df_stocks_flipped.rename(columns={"index": "date"}, inplace=True)
        df_stocks_flipped.rename(columns={"close": "close_price"}, inplace=True)

        df_stocks_flipped["date"] = df_stocks_flipped["date"]
        df_stocks_flipped.set_index("date", inplace=True)

        return df_stocks_flipped.to_dict()

    def get_nopat_2_ttm(self, ticker):
        net_income_value = self.get_net_income_ttm()

        df_dividends_paid_ttm = (
            self.df_cash_flow_quarterly["dividendsPaid"].rolling(4).sum().shift(-3)
        )
        df_dividends_paid_ttm = df_dividends_paid_ttm.dropna().to_frame()
        df_dividends_paid_ttm = df_dividends_paid_ttm.reset_index()
        df_dividends_paid_ttm.rename(columns={"index": "date"}, inplace=True)

        dividends_paid_last_date_available = df_dividends_paid_ttm["date"].max()
        dividends_paid = df_dividends_paid_ttm.loc[
            df_dividends_paid_ttm["date"] == dividends_paid_last_date_available
        ]
        try:
            dividends_paid_value = dividends_paid["dividendsPaid"].iloc[0]
        except IndexError:
            dividends_paid_value = 0.0

        print(ticker)
        print("Net Income Value: " + str(net_income_value))
        print("Dividends paid: " + str(dividends_paid_value))

    # EQUITY
    def get_equity(self):
        return float(self.df_balance_sheet_quarterly["totalStockholderEquity"].dropna().iloc[0])

    # EBITDA
    def get_ebitda(self):
        try:
            return round(self.df_highlights["EBITDA"].iloc[0], 2)
        except TypeError:
            return 0.0

    def __get_ebitda_historical(self):
        df_operating_income_ttm = (
            self.df_income_statement_quarterly["operatingIncome"].rolling(4).sum().shift(-3)
        )
        df_deprecations_ttm = self.df_cash_flow_quarterly["depreciation"].rolling(4).sum().shift(-3)

        df_operating_income_ttm = df_operating_income_ttm.to_frame()

        df_deprecations_ttm = df_deprecations_ttm.to_frame()

        df_operating_income_ttm = df_operating_income_ttm[
            df_operating_income_ttm["operatingIncome"].notna()
        ]
        df_deprecations_ttm = df_deprecations_ttm[df_deprecations_ttm["depreciation"].notna()]

        df_ebitda_ttm = df_operating_income_ttm.merge(
            df_deprecations_ttm, left_index=True, right_index=True
        )

        df_ebitda_ttm["ebitda"] = df_ebitda_ttm["operatingIncome"] + df_ebitda_ttm["depreciation"]

        return df_ebitda_ttm

    def get_ebitda_historical(self):
        return self.__get_ebitda_historical().to_dict()

    def get_ebitda_forecast(self):
        df_ebitda = self.__get_ebitda_historical()
        df_ebitda.reset_index(inplace=True)
        df_ebitda.rename(columns={"index": "date"}, inplace=True)
        df_ebitda.rename(columns={0: "ebitda"}, inplace=True)
        df_ebitda.reset_index(inplace=True)
        x = df_ebitda["index"].to_numpy()
        y = df_ebitda["ebitda"].to_numpy()

        y_future = ForecastLR.get_forecast(x, y)

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        quarter = __get_quarter(df_ebitda["date"].iloc[0])
        year = __get_year(df_ebitda["date"].iloc[0])

        forecasting_dict = dict(
            {
                "year": year,
                "quarter": quarter,
                "ebitda": float(round(df_ebitda["ebitda"].iloc[0], 2)),
            }
        )

        forecast_list = list()

        forecast_list.append(forecasting_dict)
        for j in range(0, y_future.size):
            quarter, year = Utils.get_next_quarter(quarter, year)
            forecasting_dict = dict(
                {"year": year, "quarter": quarter, "ebitda": float(round(y_future[j][0], 2)),}
            )
            forecast_list.append(forecasting_dict)

        return forecast_list

    # MARKETCAP
    def get_marketcap(self):
        try:
            return round(self.df_highlights["MarketCapitalization"].iloc[0], 2)
        except TypeError:
            return 0.0

    # TODO Review
    def get_marketcap_historical(self):
        df_stocks = self.df_stocks[["date", "close"]].iloc[::-1]
        df_shares = self.get_outstanding_shares()

        df_stocks["close"] = pd.to_numeric(df_stocks["close"])
        df_shares["shares"] = pd.to_numeric(df_shares["shares"])

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        def __get_quarter_shares(date):
            quarter = pd.Timestamp(date).quarter
            if quarter in range(1, 4):
                return quarter + 1
            elif quarter == 4:
                return 1

        def __get_year_shares(date):
            year = pd.Timestamp(date).year
            quarter = pd.Timestamp(date).quarter
            if quarter in range(1, 4):
                return year
            elif quarter == 4:
                return year + 1

        df_shares["year"] = df_shares["dateFormatted"].apply(__get_year_shares)
        df_shares["quarter"] = df_shares["dateFormatted"].apply(__get_quarter_shares)

        df_stocks["year"] = df_stocks["date"].apply(__get_year)
        df_stocks["quarter"] = df_stocks["date"].apply(__get_quarter)

        df_marketcap = df_stocks.merge(
            df_shares, how="inner", left_on=["year", "quarter"], right_on=["year", "quarter"]
        )

        df_marketcap["marketcap"] = df_marketcap["close"] * df_marketcap["shares"]

        return df_marketcap

    # OUTSTANDING SHARES
    def get_outstanding_shares(self):
        df_outstanding_shares = self.df_outstanding_shares_quarterly[["dateFormatted", "shares"]]
        return df_outstanding_shares

    # CASH
    def get_cash(self):
        return float(self.df_balance_sheet_quarterly["cash"].dropna().iloc[0])

    def get_cash_historical(self):
        df_cash = self.df_balance_sheet_quarterly["cash"].to_frame()
        df_cash.reset_index(inplace=True)
        df_cash.rename(columns={"index": "date"}, inplace=True)
        df_cash["cash"] = pd.to_numeric(df_cash["cash"])
        df_cash = df_cash.dropna()

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        df_cash["year"] = df_cash["date"].apply(__get_year)
        df_cash["quarter"] = df_cash["date"].apply(__get_quarter)

        return df_cash

    def get_cash_forecast(self):
        df_cash = self.get_cash_historical()
        df_cash.reset_index(inplace=True)
        x = df_cash["index"].to_numpy()
        y = df_cash["cash"].to_numpy()

        y_future = ForecastLR.get_forecast(x, y)

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        quarter = __get_quarter(df_cash["date"].iloc[0])
        year = __get_year(df_cash["date"].iloc[0])

        forecasting_dict = dict(
            {"year": year, "quarter": quarter, "cash": float(round(df_cash["cash"].iloc[0], 2)),}
        )

        forecast_list = list()

        forecast_list.append(forecasting_dict)
        for j in range(0, y_future.size):
            quarter, year = Utils.get_next_quarter(quarter, year)
            forecasting_dict = dict(
                {"year": year, "quarter": quarter, "cash": float(round(y_future[j][0], 2)),}
            )
            forecast_list.append(forecasting_dict)

        return forecast_list

    # TOTAL DEBT
    def get_total_debt(self):
        df_short_term_deb = self.df_balance_sheet_quarterly["shortTermDebt"]

        df_short_term_deb = df_short_term_deb.reset_index()
        df_short_term_deb.rename(columns={"index": "date"}, inplace=True)

        short_term_deb_last_date_available = df_short_term_deb["date"].max()
        short_term_deb = df_short_term_deb.loc[
            df_short_term_deb["date"] == short_term_deb_last_date_available
        ]
        try:
            short_term_deb_value = short_term_deb["shortTermDebt"].iloc[0]
        except IndexError:
            short_term_deb_value = 0.0

        df_long_term_deb = self.df_balance_sheet_quarterly["longTermDebtTotal"]

        df_long_term_deb = df_long_term_deb.reset_index()
        df_long_term_deb.rename(columns={"index": "date"}, inplace=True)

        long_term_deb_last_date_available = df_long_term_deb["date"].max()
        long_term_deb = df_long_term_deb.loc[
            df_long_term_deb["date"] == long_term_deb_last_date_available
        ]

        try:
            long_term_deb_value = long_term_deb["longTermDebtTotal"].iloc[0]
        except IndexError:
            long_term_deb_value = 0.0

        if short_term_deb_value is None:
            short_term_deb_value = 0.0

        if long_term_deb_value is None:
            long_term_deb_value = 0.0

        total_debt = float(short_term_deb_value) + float(long_term_deb_value)

        return round(total_debt, 2)

    def get_total_debt_historical(self):
        df_short_term_deb = self.df_balance_sheet_quarterly["shortTermDebt"].fillna(0).to_frame()
        df_long_term_deb = self.df_balance_sheet_quarterly["longTermDebtTotal"].fillna(0).to_frame()

        df_short_term_deb["shortTermDebt"] = pd.to_numeric(df_short_term_deb["shortTermDebt"])
        df_long_term_deb["longTermDebtTotal"] = pd.to_numeric(
            (df_long_term_deb["longTermDebtTotal"])
        )

        df_short_term_deb.reset_index(inplace=True)
        df_long_term_deb.reset_index(inplace=True)

        df_short_term_deb.rename(columns={"index": "date"}, inplace=True)
        df_long_term_deb.rename(columns={"index": "date"}, inplace=True)

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        df_short_term_deb["year"] = df_short_term_deb["date"].apply(__get_year)
        df_short_term_deb["quarter"] = df_short_term_deb["date"].apply(__get_quarter)

        df_long_term_deb["year"] = df_long_term_deb["date"].apply(__get_year)
        df_long_term_deb["quarter"] = df_long_term_deb["date"].apply(__get_quarter)

        df_total_debt = df_long_term_deb.merge(
            df_short_term_deb,
            how="inner",
            left_on=["year", "quarter"],
            right_on=["year", "quarter"],
        )

        df_total_debt["total_debt"] = (
            df_total_debt["longTermDebtTotal"] + df_total_debt["shortTermDebt"]
        )

        df_total_debt = df_total_debt.dropna()

        return df_total_debt

    def get_total_debt_forecast(self):
        df_total_debt = self.get_total_debt_historical()
        df_total_debt.reset_index(inplace=True)
        x = df_total_debt["index"].to_numpy()
        y = df_total_debt["total_debt"].to_numpy()

        y_future = ForecastLR.get_forecast(x, y)

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        quarter = __get_quarter(df_total_debt["date_y"].iloc[0])
        year = __get_year(df_total_debt["date_y"].iloc[0])

        forecasting_dict = dict(
            {
                "year": year,
                "quarter": quarter,
                "total_debt": float(round(df_total_debt["total_debt"].iloc[0], 2)),
            }
        )

        forecast_list = list()

        forecast_list.append(forecasting_dict)
        for j in range(0, y_future.size):
            quarter, year = Utils.get_next_quarter(quarter, year)
            forecasting_dict = dict(
                {"year": year, "quarter": quarter, "total_debt": float(round(y_future[j][0], 2)),}
            )
            forecast_list.append(forecasting_dict)

        return forecast_list

    # EBIT
    def get_ebit_ttm(self):
        # getting net income TTM dataframe
        df_ebit_ttm = self.df_income_statement_quarterly["ebit"].rolling(4).sum().shift(-3)

        df_ebit_ttm = df_ebit_ttm.dropna().to_frame()
        df_ebit_ttm = df_ebit_ttm.reset_index()
        df_ebit_ttm.rename(columns={"index": "date"}, inplace=True)

        ebit_ttm_last_date_available = df_ebit_ttm["date"].max()
        ebit_ttm = df_ebit_ttm.loc[df_ebit_ttm["date"] == ebit_ttm_last_date_available]
        ebit_ttm_value = ebit_ttm["ebit"].iloc[0]
        return float(ebit_ttm_value)

    def get_ebit_historical(self):
        # getting net income TTM dataframe
        df_ebit_ttm = self.df_income_statement_quarterly["ebit"].rolling(4).sum().shift(-3)

        df_ebit_ttm = df_ebit_ttm.dropna().to_frame()
        df_ebit_ttm = df_ebit_ttm.reset_index()
        df_ebit_ttm.rename(columns={"index": "date"}, inplace=True)

        return df_ebit_ttm

    def get_ebit_forecast(self):
        df_ebit = self.get_ebit_historical()
        df_ebit.reset_index(inplace=True)
        x = df_ebit["index"].to_numpy()
        y = df_ebit["ebit"].to_numpy()

        y_future = ForecastLR.get_forecast(x, y)

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        quarter = __get_quarter(df_ebit["date"].iloc[0])
        year = __get_year(df_ebit["date"].iloc[0])

        forecasting_dict = dict(
            {"year": year, "quarter": quarter, "ebit": float(round(df_ebit["ebit"].iloc[0], 2)),}
        )

        forecast_list = list()

        forecast_list.append(forecasting_dict)
        for j in range(0, y_future.size):
            quarter, year = Utils.get_next_quarter(quarter, year)
            forecasting_dict = dict(
                {"year": year, "quarter": quarter, "ebit": float(round(y_future[j][0], 2)),}
            )
            forecast_list.append(forecasting_dict)

        return forecast_list

    # Free Cash Flow FCF
    def get_fcf_historical(self):
        df_capex_ttm = self.df_cash_flow_quarterly["capitalExpenditures"].rolling(4).sum().shift(-3)
        df_interest_expense_ttm = (
            self.df_income_statement_quarterly["interestExpense"].rolling(4).sum().shift(-3)
        )
        df_income_tax_expense_ttm = (
            self.df_income_statement_quarterly["incomeTaxExpense"].rolling(4).sum().shift(-3)
        )

        df_ebitda_ttm = self.__get_ebitda_historical()

        df_capex_ttm = df_capex_ttm.to_frame()
        df_interest_expense_ttm = df_interest_expense_ttm.to_frame()
        df_income_tax_expense_ttm = df_income_tax_expense_ttm.to_frame()

        df_capex_ttm = df_capex_ttm[df_capex_ttm["capitalExpenditures"].notna()]
        df_interest_expense_ttm = df_interest_expense_ttm[
            df_interest_expense_ttm["interestExpense"].notna()
        ]
        df_income_tax_expense_ttm = df_income_tax_expense_ttm[
            df_income_tax_expense_ttm["incomeTaxExpense"].notna()
        ]

        df_capex_interest_expense = df_capex_ttm.merge(
            df_interest_expense_ttm, left_index=True, right_index=True
        )
        df_ebitda_capex_interest_expense = df_capex_interest_expense.merge(
            df_ebitda_ttm, left_index=True, right_index=True
        )
        df_fcf_ttm = df_ebitda_capex_interest_expense.merge(
            df_income_tax_expense_ttm, left_index=True, right_index=True
        )

        df_fcf_ttm["fcf"] = (
            df_fcf_ttm["ebitda"]
            - df_fcf_ttm["capitalExpenditures"]
            - df_fcf_ttm["interestExpense"]
            - df_fcf_ttm["incomeTaxExpense"]
        )

        df_fcf_ttm.reset_index(inplace=True)
        df_fcf_ttm.rename(columns={"index": "date"}, inplace=True)

        return df_fcf_ttm

    def get_fcf(self):
        return round(float(self.get_fcf_historical()["fcf"].iloc[0]), 2)

    def get_fcf_forecast(self):
        df_fcf = self.get_fcf_historical()
        df_fcf.reset_index(inplace=True)
        x = df_fcf["index"].to_numpy()
        y = df_fcf["fcf"].to_numpy()

        y_future = ForecastLR.get_forecast(x, y)

        def __get_year(date):
            return pd.Timestamp(date).year

        def __get_quarter(date):
            return pd.Timestamp(date).quarter

        quarter = __get_quarter(df_fcf["date"].iloc[0])
        year = __get_year(df_fcf["date"].iloc[0])

        forecasting_dict = dict(
            {"year": year, "quarter": quarter, "fcf": float(round(df_fcf["fcf"].iloc[0], 2)),}
        )

        forecast_list = list()

        forecast_list.append(forecasting_dict)
        for j in range(0, y_future.size):
            quarter, year = Utils.get_next_quarter(quarter, year)
            forecasting_dict = dict(
                {"year": year, "quarter": quarter, "fcf": float(round(y_future[j][0], 2)),}
            )
            forecast_list.append(forecasting_dict)

        return forecast_list

    # NET INCOME
    def get_net_income_ttm(self):
        df_net_income_ttm = self.get_net_income_historical()

        if df_net_income_ttm.empty:
            return self.df_highlights["EarningsShare"].iloc[0], 0.0, 0.0
        else:
            return self.get_net_income_historical()["netIncome"].iloc[0]

    def get_net_income_historical(self):
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

            return df_net_income_ttm

        else:
            return df_net_income_ttm

    def get_net_income_forecast(self):
        df_net_income_historical = self.get_net_income_historical()

        x = df_net_income_historical["date"].to_numpy()
        y = df_net_income_historical["netIncome"].to_numpy()

        y_future = ForecastLR.get_forecast(x, y)

        fecha = df_net_income_historical["date"].iloc[0]
        quarter = pd.Timestamp(fecha).quarter
        year = pd.Timestamp(fecha).year
        # quarter, year = fecha.quarter, fecha.year
        forecast_list = list()
        forecasting_dict = dict(
            {
                "year": year,
                "quarter": quarter,
                "netIncome": float(round(df_net_income_historical["netIncome"].iloc[0], 2)),
            }
        )
        forecast_list.append(forecasting_dict)
        for j in range(0, y_future.size):
            quarter, year = Utils.get_next_quarter(quarter, year)
            forecasting_dict = dict(
                {"year": year, "quarter": quarter, "netIncome": float(round(y_future[j][0], 2)),}
            )
            forecast_list.append(forecasting_dict)

        return forecast_list
