# Generated by Django 2.1.15 on 2020-11-14 22:13

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('ticker', models.CharField(max_length=32, unique=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('stock_price', models.FloatField(blank=True, default=None, null=True)),
                ('eps_diluted_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('eps_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('price_book_mqr', models.FloatField(blank=True, default=None, null=True)),
                ('per_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('per_forward', models.FloatField(blank=True, default=None, null=True)),
                ('peg', models.FloatField(blank=True, default=None, null=True)),
                ('roe_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('roa_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('ebitda', models.FloatField(blank=True, default=None, null=True)),
                ('ebit_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('total_debt', models.FloatField(blank=True, default=None, null=True)),
                ('equity', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebitda', models.FloatField(blank=True, default=None, null=True)),
                ('marketcap', models.FloatField(blank=True, default=None, null=True)),
                ('cash', models.FloatField(blank=True, default=None, null=True)),
                ('wall_street_target_price', models.FloatField(blank=True, default=None, null=True)),
                ('roic_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('enterprise_value', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebit', models.FloatField(blank=True, default=None, null=True)),
                ('fcf_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('ev_fcf', models.FloatField(blank=True, default=None, null=True)),
                ('net_income_forecast', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('eps_forecast', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('stock_price_historical', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('eps_historical', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('enterprise_value_historical', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'company',
                'verbose_name_plural': 'companies',
                'db_table': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=32, unique=True)),
                ('rate', models.FloatField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
                'db_table': 'currencies',
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('trailing_pe', models.FloatField(blank=True, default=None, null=True)),
                ('per_forward', models.FloatField(blank=True, default=None, null=True)),
                ('price_book_mqr', models.FloatField(blank=True, default=None, null=True)),
                ('return_on_equity_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('return_on_assets_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('roic_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebit', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebitda', models.FloatField(blank=True, default=None, null=True)),
                ('ev_fcf', models.FloatField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'exchange',
                'verbose_name_plural': 'exchanges',
                'db_table': 'exchanges',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('trailing_pe', models.FloatField(blank=True, default=None, null=True)),
                ('per_forward', models.FloatField(blank=True, default=None, null=True)),
                ('price_book_mqr', models.FloatField(blank=True, default=None, null=True)),
                ('return_on_equity_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('return_on_assets_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('roic_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebit', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebitda', models.FloatField(blank=True, default=None, null=True)),
                ('ev_fcf', models.FloatField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'industry',
                'verbose_name_plural': 'industries',
                'db_table': 'industries',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('trailing_pe', models.FloatField(blank=True, default=None, null=True)),
                ('per_forward', models.FloatField(blank=True, default=None, null=True)),
                ('price_book_mqr', models.FloatField(blank=True, default=None, null=True)),
                ('return_on_equity_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('return_on_assets_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('roic_ttm', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebit', models.FloatField(blank=True, default=None, null=True)),
                ('ev_ebitda', models.FloatField(blank=True, default=None, null=True)),
                ('ev_fcf', models.FloatField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'sector',
                'verbose_name_plural': 'sectors',
                'db_table': 'sectors',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='exchange',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Exchange'),
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Industry'),
        ),
        migrations.AddField(
            model_name='company',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Sector'),
        ),
    ]
