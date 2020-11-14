# -*- encoding: utf-8 -*-
"""
License: Commercial
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

import uuid

from django.contrib.postgres.fields.jsonb import JSONField


class Industry(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    trailing_pe = models.FloatField(null=True, blank=True, default=None)
    per_forward = models.FloatField(null=True, blank=True, default=None)
    price_book_mqr = models.FloatField(null=True, blank=True, default=None)
    return_on_equity_ttm = models.FloatField(null=True, blank=True, default=None)
    return_on_assets_ttm = models.FloatField(null=True, blank=True, default=None)
    roic_ttm = models.FloatField(null=True, blank=True, default=None)
    ev_ebit = models.FloatField(null=True, blank=True, default=None)
    ev_ebitda = models.FloatField(null=True, blank=True, default=None)
    ev_fcf = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = "industries"
        verbose_name = "industry"
        verbose_name_plural = "industries"

    def __str__(self):
        return f"{ self.name }"

    def __repr__(self):
        return f"Industry(name={ self.name })"


class Sector(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    trailing_pe = models.FloatField(null=True, blank=True, default=None)
    per_forward = models.FloatField(null=True, blank=True, default=None)
    price_book_mqr = models.FloatField(null=True, blank=True, default=None)
    return_on_equity_ttm = models.FloatField(null=True, blank=True, default=None)
    return_on_assets_ttm = models.FloatField(null=True, blank=True, default=None)
    roic_ttm = models.FloatField(null=True, blank=True, default=None)
    ev_ebit = models.FloatField(null=True, blank=True, default=None)
    ev_ebitda = models.FloatField(null=True, blank=True, default=None)
    ev_fcf = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = "sectors"
        verbose_name = "sector"
        verbose_name_plural = "sectors"

    def __str__(self):
        return f"{ self.name }"

    def __repr__(self):
        return f"Sector(name={ self.name })"


class Exchange(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    trailing_pe = models.FloatField(null=True, blank=True, default=None)
    per_forward = models.FloatField(null=True, blank=True, default=None)
    price_book_mqr = models.FloatField(null=True, blank=True, default=None)
    return_on_equity_ttm = models.FloatField(null=True, blank=True, default=None)
    return_on_assets_ttm = models.FloatField(null=True, blank=True, default=None)
    roic_ttm = models.FloatField(null=True, blank=True, default=None)
    ev_ebit = models.FloatField(null=True, blank=True, default=None)
    ev_ebitda = models.FloatField(null=True, blank=True, default=None)
    ev_fcf = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = "exchanges"
        verbose_name = "exchange"
        verbose_name_plural = "exchanges"

    def __str__(self):
        return f"{ self.name }"

    def __repr__(self):
        return f"Exchange(name={ self.name })"


class Currency(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    code = models.CharField(max_length=32, unique=True)
    rate = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = "currencies"
        verbose_name = "currency"
        verbose_name_plural = "currencies"

    def __str__(self):
        return f"{ self.code }"

    def __repr__(self):
        return f"Currency(name={ self.code })"


class Company(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ticker = models.CharField(max_length=32, unique=True)
    data = JSONField(blank=True, null=True)
    stock_price = models.FloatField(null=True, blank=True, default=None)
    eps_diluted_ttm = models.FloatField(null=True, blank=True, default=None)
    eps_ttm = models.FloatField(null=True, blank=True, default=None)
    price_book_mqr = models.FloatField(null=True, blank=True, default=None)
    per_ttm = models.FloatField(null=True, blank=True, default=None)
    per_forward = models.FloatField(null=True, blank=True, default=None)
    peg = models.FloatField(null=True, blank=True, default=None)
    roe_ttm = models.FloatField(null=True, blank=True, default=None)
    roa_ttm = models.FloatField(null=True, blank=True, default=None)
    ebitda = models.FloatField(null=True, blank=True, default=None)
    ebit_ttm = models.FloatField(null=True, blank=True, default=None)
    total_debt = models.FloatField(null=True, blank=True, default=None)
    equity = models.FloatField(null=True, blank=True, default=None)
    ev_ebitda = models.FloatField(null=True, blank=True, default=None)
    marketcap = models.FloatField(null=True, blank=True, default=None)
    cash = models.FloatField(null=True, blank=True, default=None)
    wall_street_target_price = models.FloatField(null=True, blank=True, default=None)
    roic_ttm = models.FloatField(null=True, blank=True, default=None)
    enterprise_value = models.FloatField(null=True, blank=True, default=None)
    ev_ebit = models.FloatField(null=True, blank=True, default=None)
    fcf_ttm = models.FloatField(null=True, blank=True, default=None)
    ev_fcf = models.FloatField(null=True, blank=True, default=None)
    net_income_forecast = JSONField(blank=True, null=True)
    eps_forecast = JSONField(blank=True, null=True)
    stock_price_historical = JSONField(blank=True, null=True)
    eps_historical = JSONField(blank=True, null=True)
    enterprise_value_historical = JSONField(blank=True, null=True)
    exchange = models.ForeignKey(Exchange, models.CASCADE)
    sector = models.ForeignKey(Sector, models.CASCADE)
    industry = models.ForeignKey(Industry, models.CASCADE)

    class Meta:
        db_table = "companies"
        verbose_name = "company"
        verbose_name_plural = "companies"

    def __str__(self):
        return f"{ self.id }, { self.ticker }"

    def __repr__(self):
        return f"Company(id={ self.id }, ticker={ self.ticker })"
