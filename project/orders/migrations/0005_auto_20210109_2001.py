# Generated by Django 3.1.5 on 2021-01-09 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210109_1959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_date',
            new_name='date',
        ),
    ]
