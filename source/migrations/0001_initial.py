# Generated by Django 5.1.1 on 2024-10-21 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricDayModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.IntegerField(db_index=True)),
                ('open', models.DecimalField(decimal_places=2, max_digits=17)),
                ('high', models.DecimalField(decimal_places=2, max_digits=17)),
                ('low', models.DecimalField(decimal_places=2, max_digits=17)),
                ('close', models.DecimalField(decimal_places=2, max_digits=17)),
                ('volume', models.IntegerField()),
                ('created', models.IntegerField()),
                ('updated', models.IntegerField()),
            ],
            options={
                'db_table': 'historical_day',
            },
        ),
        migrations.CreateModel(
            name='StockModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('api', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=255)),
                ('industry', models.CharField(max_length=255)),
                ('timezone', models.IntegerField()),
                ('fingerprint', models.TextField(max_length=65535)),
                ('created', models.IntegerField()),
                ('updated', models.IntegerField()),
            ],
            options={
                'db_table': 'stocks',
            },
        ),
        migrations.CreateModel(
            name='ProphesyDayModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField(db_index=True)),
                ('increased_day', models.IntegerField(db_index=True)),
                ('data_end_date', models.IntegerField(db_index=True)),
                ('data_start_date', models.IntegerField(db_index=True)),
                ('date', models.IntegerField(db_index=True)),
                ('trend', models.DecimalField(decimal_places=2, max_digits=17)),
                ('yhat_lower', models.DecimalField(decimal_places=2, max_digits=17)),
                ('yhat_upper', models.DecimalField(decimal_places=2, max_digits=17)),
                ('trend_lower', models.DecimalField(decimal_places=2, max_digits=17)),
                ('trend_upper', models.DecimalField(decimal_places=2, max_digits=17)),
                ('additive_terms', models.DecimalField(decimal_places=2, max_digits=17)),
                ('additive_terms_lower', models.DecimalField(decimal_places=2, max_digits=17)),
                ('additive_terms_upper', models.DecimalField(decimal_places=2, max_digits=17)),
                ('weekly', models.DecimalField(decimal_places=2, max_digits=17)),
                ('weekly_lower', models.DecimalField(decimal_places=2, max_digits=17)),
                ('weekly_upper', models.DecimalField(decimal_places=2, max_digits=17)),
                ('multiplicative_terms', models.DecimalField(decimal_places=2, max_digits=17)),
                ('multiplicative_terms_lower', models.DecimalField(decimal_places=2, max_digits=17)),
                ('multiplicative_terms_upper', models.DecimalField(decimal_places=2, max_digits=17)),
                ('yhat', models.DecimalField(decimal_places=2, max_digits=17)),
                ('created', models.IntegerField()),
                ('updated', models.IntegerField()),
                ('last_historic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.historicdaymodel')),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.stockmodel')),
            ],
            options={
                'db_table': 'prophesied_day',
            },
        ),
        migrations.CreateModel(
            name='ProphesyForecastDayModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.IntegerField(db_index=True)),
                ('type', models.IntegerField(db_index=True)),
                ('value_historic', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('value_forecast', models.DecimalField(decimal_places=2, max_digits=17)),
                ('difference_historic', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('percentage_historic', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('difference_forecast', models.DecimalField(decimal_places=2, max_digits=17)),
                ('percentage_forecast', models.DecimalField(decimal_places=2, max_digits=17)),
                ('qualitative_forecast', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('quantitative_forecast', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('created', models.IntegerField()),
                ('updated', models.IntegerField()),
                ('historic_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='source.historicdaymodel')),
                ('prophesy_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.prophesydaymodel')),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.stockmodel')),
            ],
            options={
                'db_table': 'prophesy_forecasts_day',
            },
        ),
        migrations.AddField(
            model_name='historicdaymodel',
            name='stock_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.stockmodel'),
        ),
    ]
