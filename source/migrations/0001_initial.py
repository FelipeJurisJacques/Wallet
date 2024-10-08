# Generated by Django 5.1.1 on 2024-10-08 23:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=255, unique=True)),
                ('industry', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'stocks',
            },
        ),
        migrations.CreateModel(
            name='HistoricEntity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.IntegerField()),
                ('open', models.DecimalField(decimal_places=2, max_digits=10)),
                ('high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('close', models.DecimalField(decimal_places=2, max_digits=10)),
                ('volume', models.IntegerField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.stockentity')),
            ],
            options={
                'db_table': 'historical',
            },
        ),
    ]
