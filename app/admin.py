# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from app.models import Company
from app.models import Industry
from app.models import Sector
from app.models import Exchange
from app.models import Currency


@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "ticker",
        "get_exchange_name",
        "get_sector_name",
        "get_industry_name",
        "stock_price",
        "eps_ttm",
        "eps_diluted_ttm",
        "price_book_mqr",
        "per_ttm",
        "per_forward",
        "peg",
        "roe_ttm",
        "roa_ttm",
        "roic_ttm",
        "ebitda",
        "ebit_ttm",
        "fcf_ttm",
        "total_debt",
        "equity",
        "ev_ebitda",
        "ev_ebit",
        "ev_fcf",
        "marketcap",
        "cash",
        "wall_street_target_price",
        "enterprise_value",
    )

    def get_exchange_name(self, obj):
        return obj.exchange.name

    def get_sector_name(self, obj):
        return obj.sector.name

    def get_industry_name(self, obj):
        return obj.industry.name

    get_exchange_name.short_description = "EXCHANGE"
    get_sector_name.short_description = "SECTOR"
    get_industry_name.short_description = "INDUSTRY"


@admin.register(Industry)
class IndustryAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "trailing_pe",
        "per_forward",
        "price_book_mqr",
        "return_on_equity_ttm",
        "return_on_assets_ttm",
        "roic_ttm",
        "ev_ebitda",
        "ev_ebit",
        "ev_fcf",
    )


@admin.register(Sector)
class SectorAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "trailing_pe",
        "per_forward",
        "price_book_mqr",
        "return_on_equity_ttm",
        "return_on_assets_ttm",
        "roic_ttm",
        "ev_ebitda",
        "ev_ebit",
        "ev_fcf",
    )


@admin.register(Exchange)
class ExchangeAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "trailing_pe",
        "per_forward",
        "price_book_mqr",
        "return_on_equity_ttm",
        "return_on_assets_ttm",
        "roic_ttm",
        "ev_ebitda",
        "ev_ebit",
        "ev_fcf",
    )


@admin.register(Currency)
class CurrencyAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "code",
        "rate",
    )
