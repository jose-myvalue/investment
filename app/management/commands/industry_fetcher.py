from app.models import Company
from app.models import Exchange
from app.models import Sector
from app.models import Industry
import pandas as pd
import numpy as np
from django.core.management import BaseCommand

from scipy.stats import zscore


def remove_outliers(df, columns):
    df_clean = df.dropna()
    for column in columns:
        try:
            df_clean = df_clean[(np.abs(zscore(df_clean[column])) < 3)]
        except ZeroDivisionError:
            return df
    return df_clean


class Command(BaseCommand):
    def handle(self, *args, **options):
        companies_objects = Company.objects.all()

        exchanges = set()
        sectors = set()
        industries = set()

        companies_list = list()

        for company in companies_objects:
            print(company.ticker)
            company_row = (
                company.ticker,
                Exchange.objects.get(id=company.exchange.id).name,
                Sector.objects.get(id=company.sector.id).name,
                Industry.objects.get(id=company.industry.id).name,
                company.per_ttm,
                company.per_forward,
                company.price_book_mqr,
                company.roe_ttm,
                company.roa_ttm,
                company.roic_ttm,
                company.ev_ebit,
                company.ev_ebitda,
                company.ev_fcf,
            )
            companies_list.append(company_row)

            exchanges.add(Exchange.objects.get(id=company.exchange.id).name)
            sectors.add(Sector.objects.get(id=company.sector.id).name)
            industries.add(Industry.objects.get(id=company.industry.id).name)

        companies_df = pd.DataFrame(
            companies_list,
            columns=[
                "code",
                "exchange",
                "sector",
                "industry",
                "TrailingPE",
                "ForwardPE",
                "PriceBookMRQ",
                "ReturnOnEquityTTM",
                "ReturnOnAssetsTTM",
                "RoicTTM",
                "EVEBIT",
                "EVEBITDA",
                "EVFCF",
            ],
        )

        companies_df = remove_outliers(
            companies_df,
            [
                "TrailingPE",
                "ForwardPE",
                "PriceBookMRQ",
                "ReturnOnEquityTTM",
                "ReturnOnAssetsTTM",
                "RoicTTM",
                "EVEBIT",
                "EVEBITDA",
                "EVFCF",
            ],
        )

        exchanges_list = list()

        for exchange in exchanges:
            exchages_row = (
                exchange,
                companies_df.loc[companies_df["exchange"] == exchange]["TrailingPE"].median(),
                companies_df.loc[companies_df["exchange"] == exchange]["ForwardPE"].median(),
                companies_df.loc[companies_df["exchange"] == exchange]["PriceBookMRQ"].median(),
                companies_df.loc[companies_df["exchange"] == exchange][
                    "ReturnOnEquityTTM"
                ].median(),
                companies_df.loc[companies_df["exchange"] == exchange][
                    "ReturnOnAssetsTTM"
                ].median(),
                companies_df.loc[companies_df["exchange"] == exchange]["RoicTTM"].median(),
                companies_df.loc[companies_df["exchange"] == exchange]["EVEBIT"].median(),
                companies_df.loc[companies_df["exchange"] == exchange]["EVEBITDA"].median(),
                companies_df.loc[companies_df["exchange"] == exchange]["EVFCF"].median(),
            )
            exchanges_list.append(exchages_row)

        exchanges_df = pd.DataFrame(
            exchanges_list,
            columns=[
                "exchange",
                "TrailingPE",
                "ForwardPE",
                "PriceBookMRQ",
                "ReturnOnEquityTTM",
                "ReturnOnAssetsTTM",
                "RoicTTM",
                "EVEBIT",
                "EVEBITDA",
                "EVFCF",
            ],
        )

        for exchange in exchanges:
            ex_list = exchanges_df.loc[exchanges_df["exchange"] == exchange]
            ex, created = Exchange.objects.get_or_create(name=exchange)
            ex.name = ex_list["exchange"].values[0]
            ex.trailing_pe = round(ex_list["TrailingPE"].values[0], 2)
            ex.per_forward = round(ex_list["ForwardPE"].values[0], 2)
            ex.price_book_mqr = ex_list["PriceBookMRQ"].values[0]
            ex.return_on_equity_ttm = ex_list["ReturnOnEquityTTM"].values[0]
            ex.return_on_assets_ttm = ex_list["ReturnOnAssetsTTM"].values[0]
            ex.roic_ttm = round(ex_list["RoicTTM"].values[0], 2)
            ex.ev_ebit = round(ex_list["EVEBIT"].values[0], 2)
            ex.ev_ebitda = round(ex_list["EVEBITDA"].values[0], 2)
            ex.ev_fcf = round(ex_list["EVFCF"].values[0], 2)
            ex.save()

        sector_list = list()

        for sector in sectors:
            sector_row = (
                sector,
                companies_df.loc[companies_df["sector"] == sector]["TrailingPE"].median(),
                companies_df.loc[companies_df["sector"] == sector]["ForwardPE"].median(),
                companies_df.loc[companies_df["sector"] == sector]["PriceBookMRQ"].median(),
                companies_df.loc[companies_df["sector"] == sector]["ReturnOnEquityTTM"].median(),
                companies_df.loc[companies_df["sector"] == sector]["ReturnOnAssetsTTM"].median(),
                companies_df.loc[companies_df["sector"] == sector]["RoicTTM"].median(),
                companies_df.loc[companies_df["sector"] == sector]["EVEBIT"].median(),
                companies_df.loc[companies_df["sector"] == sector]["EVEBITDA"].median(),
                companies_df.loc[companies_df["sector"] == sector]["EVFCF"].median(),
            )
            sector_list.append(sector_row)

        sector_df = pd.DataFrame(
            sector_list,
            columns=[
                "sector",
                "TrailingPE",
                "ForwardPE",
                "PriceBookMRQ",
                "ReturnOnEquityTTM",
                "ReturnOnAssetsTTM",
                "RoicTTM",
                "EVEBIT",
                "EVEBITDA",
                "EVFCF",
            ],
        )

        for sector in sectors:
            sec_list = sector_df.loc[sector_df["sector"] == sector]
            sec, created = Sector.objects.get_or_create(name=sector)
            sec.name = sec_list["sector"].values[0]
            sec.trailing_pe = round(sec_list["TrailingPE"].values[0], 2)
            sec.per_forward = round(sec_list["ForwardPE"].values[0], 2)
            sec.price_book_mqr = sec_list["PriceBookMRQ"].values[0]
            sec.return_on_equity_ttm = sec_list["ReturnOnEquityTTM"].values[0]
            sec.return_on_assets_ttm = sec_list["ReturnOnAssetsTTM"].values[0]
            sec.roic_ttm = round(sec_list["RoicTTM"].values[0], 2)
            sec.ev_ebit = round(sec_list["EVEBIT"].values[0], 2)
            sec.ev_ebitda = round(sec_list["EVEBITDA"].values[0], 2)
            sec.ev_fcf = round(sec_list["EVFCF"].values[0], 2)
            sec.save()

        industry_list = list()

        for industry in industries:
            industry_row = (
                industry,
                companies_df.loc[companies_df["industry"] == industry]["TrailingPE"].median(),
                companies_df.loc[companies_df["industry"] == industry]["ForwardPE"].median(),
                companies_df.loc[companies_df["industry"] == industry]["PriceBookMRQ"].median(),
                companies_df.loc[companies_df["industry"] == industry][
                    "ReturnOnEquityTTM"
                ].median(),
                companies_df.loc[companies_df["industry"] == industry][
                    "ReturnOnAssetsTTM"
                ].median(),
                companies_df.loc[companies_df["industry"] == industry]["RoicTTM"].median(),
                companies_df.loc[companies_df["industry"] == industry]["EVEBIT"].median(),
                companies_df.loc[companies_df["industry"] == industry]["EVEBITDA"].median(),
                companies_df.loc[companies_df["industry"] == industry]["EVFCF"].median(),
            )
            industry_list.append(industry_row)

        industry_df = pd.DataFrame(
            industry_list,
            columns=[
                "industry",
                "TrailingPE",
                "ForwardPE",
                "PriceBookMRQ",
                "ReturnOnEquityTTM",
                "ReturnOnAssetsTTM",
                "RoicTTM",
                "EVEBIT",
                "EVEBITDA",
                "EVFCF",
            ],
        )

        for industry in industries:
            ind_list = industry_df.loc[industry_df["industry"] == industry]
            ind, created = Industry.objects.get_or_create(name=industry)
            ind.name = ind_list["industry"].values[0]
            ind.trailing_pe = round(ind_list["TrailingPE"].values[0], 2)
            ind.per_forward = round(ind_list["ForwardPE"].values[0], 2)
            ind.price_book_mqr = ind_list["PriceBookMRQ"].values[0]
            ind.return_on_equity_ttm = ind_list["ReturnOnEquityTTM"].values[0]
            ind.return_on_assets_ttm = ind_list["ReturnOnAssetsTTM"].values[0]
            ind.roic_ttm = round(ind_list["RoicTTM"].values[0], 2)
            ind.ev_ebit = round(ind_list["EVEBIT"].values[0], 2)
            ind.ev_ebitda = round(ind_list["EVEBITDA"].values[0], 2)
            ind.ev_fcf = round(ind_list["EVFCF"].values[0], 2)
            ind.save()
