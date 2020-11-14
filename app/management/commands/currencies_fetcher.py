from forex_python.converter import CurrencyRates
from app.models import Currency

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        c = CurrencyRates()

        currency_rates = c.get_rates("USD")

        for currency in currency_rates:
            currency_rate, created = Currency.objects.get_or_create(code=currency)
            currency_rate.code = currency
            currency_rate.rate = currency_rates[currency]
            currency_rate.save()
