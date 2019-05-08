# Generated by Django 2.1.7 on 2019-05-01 10:30

from django.db import migrations
import lily.base.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20190318_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogueitem',
            name='executor_type',
            field=lily.base.models.EnumChoiceField(
                choices=[
                    ('DATABRICKS', 'DATABRICKS'),
                    ('ATHENA', 'ATHENA'),
                ],
                enum_name='Executor',
                max_length=256),
        ),
    ]
