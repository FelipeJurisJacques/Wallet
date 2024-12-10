# Generated by Django 5.1.1 on 2024-12-10 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField()),
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
                'db_table': 'historical',
            },
        ),
        migrations.CreateModel(
            name='PeriodModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('period', models.IntegerField(db_index=True)),
                ('created', models.IntegerField()),
                ('updated', models.IntegerField()),
                ('historical', models.ManyToManyField(db_index=True, to='source.historicmodel')),
            ],
            options={
                'db_table': 'periods',
            },
        ),
        migrations.CreateModel(
            name='ForecastModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField(db_index=True)),
                ('forecast_min_value', models.DecimalField(decimal_places=2, max_digits=17)),
                ('forecast_max_value', models.DecimalField(decimal_places=2, max_digits=17)),
                ('forecast_min_moment', models.IntegerField()),
                ('forecast_max_moment', models.IntegerField()),
                ('forecast_difference', models.DecimalField(decimal_places=2, max_digits=17)),
                ('forecast_percentage', models.DecimalField(decimal_places=2, max_digits=17)),
                ('corrected_min_value', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('corrected_max_value', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('corrected_min_moment', models.IntegerField(blank=True, null=True)),
                ('corrected_max_moment', models.IntegerField(blank=True, null=True)),
                ('corrected_difference', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('corrected_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('created', models.IntegerField()),
                ('updated', models.IntegerField()),
                ('period', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.periodmodel')),
            ],
            options={
                'db_table': 'forecasts',
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
                'unique_together': {('api', 'symbol')},
            },
        ),
        migrations.AddField(
            model_name='historicmodel',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.stockmodel'),
        ),
        migrations.CreateModel(
            name='StrategyModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qualitative', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('quantitative', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('created', models.IntegerField()),
                ('updated', models.IntegerField()),
                ('period', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='source.periodmodel')),
            ],
            options={
                'db_table': 'strategies',
            },
        ),
        migrations.CreateModel(
            name='ProphesyModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField(db_index=True)),
                ('increased', models.IntegerField(db_index=True)),
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
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.periodmodel')),
            ],
            options={
                'db_table': 'prophesied',
                'unique_together': {('type', 'period', 'increased')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='historicmodel',
            unique_together={('type', 'date', 'stock')},
        ),
    ]
