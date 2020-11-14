import json
import logging
import multiprocessing
import urllib
from datetime import datetime
from queue import Queue
from threading import Thread
from time import time
from urllib.request import urlopen

import requests
from django.conf import settings
from django.core.management import BaseCommand

from app.models import Company
from app.value.fundamentals import Fundamentals
from app.value.returns import Returns
from app.value.ratios import Ratios
from app.value.company_information import CompanyInformation

eod_fundamentals_url = "https://eodhistoricaldata.com/api/fundamentals"
eod_stocks_url = "https://eodhistoricaldata.com/api/eod/"
eod_api_key = "5ed777c9e987b0.28049650"

logger = logging.getLogger(__name__)

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            company = self.queue.get()
            ticker_name = company.ticker
            print(ticker_name)
            url_fundamentals = f"{eod_fundamentals_url}/{ticker_name}/?api_token={eod_api_key}"
            url_stocks = f"{eod_stocks_url}/{ticker_name}?from=2015-01-01&to={str(datetime.today().date())}&api_token={eod_api_key}&period=d&fmt=json"  # noqa

            try:
                try:
                    response_fundamentals = urlopen(url_fundamentals)
                    data_fundamentals = response_fundamentals.read().decode("utf-8")
                    fundamentals_data = json.loads(data_fundamentals)
                except urllib.error.URLError:
                    print(url_fundamentals)
                    print(ticker_name + " timeout, we will try again")
                    try:
                        response_fundamentals = urlopen(url_fundamentals)
                        data_fundamentals = response_fundamentals.read().decode("utf-8")
                        fundamentals_data = json.loads(data_fundamentals)
                    except urllib.error.URLError:
                        fundamentals_data = {}
                        print("Second Try failed again, looks it doesn't exits")

                try:
                    response_stocks = urlopen(url_stocks)
                    data_stocks = response_stocks.read().decode("utf-8")
                    stocks_data = json.loads(data_stocks)
                except urllib.error.URLError:
                    print(url_stocks)
                    print(ticker_name + " timeout, we will try again")
                    try:
                        response_stocks = urlopen(url_stocks)
                        data_stocks = response_stocks.read().decode("utf-8")
                        stocks_data = json.loads(data_stocks)
                    except urllib.error.URLError:
                        stocks_data = {}
                        print("Second Try failed again, looks it doesn't exits")

                data = {}

                try:
                    data["General"] = fundamentals_data["General"]
                except KeyError:
                    print(str(ticker_name) + " json is empty")
                    continue

                try:
                    data["ESGScores"] = fundamentals_data["ESGScores"]
                except KeyError as err:
                    print(str(err) + " not available")

                try:
                    data["highlights"] = fundamentals_data["Highlights"]
                except KeyError:
                    print(str(ticker_name) + " has not highligths")
                    continue

                try:
                    data["valuation"] = fundamentals_data["Valuation"]
                except KeyError:
                    print(str(ticker_name) + " has not valuation")
                    continue

                data["quarters_cash_flow"] = fundamentals_data["Financials"]["Cash_Flow"][
                    "quarterly"
                ]
                data["shares_stats"] = fundamentals_data["SharesStats"]
                data["outstanding-shares-annual"] = fundamentals_data["outstandingShares"]["annual"]
                data["outstanding-shares-quarterly"] = fundamentals_data["outstandingShares"][
                    "quarterly"
                ]
                data["quarters_balance_sheet"] = fundamentals_data["Financials"]["Balance_Sheet"][
                    "quarterly"
                ]
                data["quarters_income_statement"] = fundamentals_data["Financials"][
                    "Income_Statement"
                ]["quarterly"]
                data["quarters_shares"] = fundamentals_data["outstandingShares"]["quarterly"]

                data["yearly_cash_flow"] = fundamentals_data["Financials"]["Cash_Flow"]["yearly"]
                data["yearly_balance_sheet"] = fundamentals_data["Financials"]["Balance_Sheet"][
                    "yearly"
                ]
                data["yearly_income_statement"] = fundamentals_data["Financials"][
                    "Income_Statement"
                ]["yearly"]

                data["Stocks"] = dict()
                for stock_price_date in stocks_data:
                    data["Stocks"][stock_price_date["date"]] = stock_price_date

                if bool(data["quarters_income_statement"]):
                    company_fundamentals = Fundamentals(data)
                    company_returns = Returns(data)
                    company_ratios = Ratios(data)

                    company.data = data

                    company.ebitda = company_fundamentals.get_ebitda()
                    company.total_debt = company_fundamentals.get_total_debt()
                    company.equity = company_fundamentals.get_equity()
                    company.fcf_ttm = company_fundamentals.get_fcf()
                    company.marketcap = company_fundamentals.get_marketcap()
                    company.cash = company_fundamentals.get_cash()
                    company.ebit_ttm = company_fundamentals.get_ebit_ttm()
                    company.net_income_forecast = company_fundamentals.get_net_income_forecast()
                    company.stock_price = company_fundamentals.get_stock_price()
                    company.stock_price_historical = (
                        company_fundamentals.get_historical_stock_price()
                    )
                    company_fundamentals.get_fcf_forecast()

                    company.price_book_mqr = company_ratios.get_price_book_mqr()
                    company.per_ttm = company_ratios.get_per_ttm()
                    company.per_forward = company_ratios.get_per_forward()
                    company.ev_ebitda = company_ratios.get_ev_ebitda()
                    company.peg = company_ratios.get_peg()
                    company.eps_diluted_ttm = company_ratios.get_eps_diluted_ttm()
                    company.eps_ttm = company_ratios.get_eps_ttm()
                    company.wall_street_target_price = company_ratios.get_wall_street_target_price()
                    company.enterprise_value = company_ratios.get_enterprise_value()
                    company.ev_ebit = company_ratios.get_ev_ebit()
                    company.ev_fcf = company_ratios.get_ev_fcf()
                    company.eps_forecast = company_ratios.get_eps_forecast()
                    company.eps_historical = company_ratios.get_eps_historical()
                    company.enterprise_value_historical = (
                        company_ratios.get_enterprise_value_historical()
                    )
                    print("Price EV/FCF")
                    print(company_ratios.get_price_ev_fcf_forecast().head(10))
                    print("Price EV/EBIT")
                    print(company_ratios.get_price_ev_ebit_forecast().head(10))
                    print("Price EV/EBITDA")
                    print(company_ratios.get_price_ev_ebitda_forecast().head(10))

                    per_dict = company_ratios.get_historical_per()
                    data["cualify_per"] = per_dict["per"]

                    company.roe_ttm = company_returns.get_roe_ttm()
                    company.roa_ttm = company_returns.get_roa_ttm()
                    company.roic_ttm = company_returns.get_roic_ttm()

                    company_information = CompanyInformation(data)
                    company.exchange = company_information.get_exchange()
                    company.save()
            finally:
                self.queue.task_done()


class Command(BaseCommand):
    def handle(self, *args, **options):
        ts = time()
        queue = Queue()

        companies = Company.objects.all()

        for company in companies:
            queue.put(company)

        thread_count = settings.COMMAND_MAX_THREADS_COUNT or multiprocessing.cpu_count()
        for x in range(thread_count):
            worker = DownloadWorker(queue)
            worker.daemon = True
            worker.start()

        queue.join()
        total_time = time() - ts
        print(f"Total processing time: {total_time}")
