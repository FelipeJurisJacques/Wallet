# Generated by Django 5.1.1 on 2025-01-05 21:44

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
                ('min_date', models.IntegerField()),
                ('max_date', models.IntegerField()),
                ('interval', models.IntegerField()),
                ('min_value', models.DecimalField(decimal_places=2, max_digits=17)),
                ('max_value', models.DecimalField(decimal_places=2, max_digits=17)),
                ('difference', models.DecimalField(decimal_places=2, max_digits=17)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=17)),
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
                ('trend', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('yhat_lower', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('yhat_upper', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('trend_lower', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('trend_upper', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('additive_terms', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('additive_terms_lower', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('additive_terms_upper', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('weekly', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('weekly_lower', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('weekly_upper', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('multiplicative_terms', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('multiplicative_terms_lower', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('multiplicative_terms_upper', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
                ('yhat', models.DecimalField(blank=True, decimal_places=2, max_digits=17, null=True)),
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
