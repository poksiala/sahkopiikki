# Generated by Django 2.0.5 on 2018-05-09 13:22

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_transaction_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
