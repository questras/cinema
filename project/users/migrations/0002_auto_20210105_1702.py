# Generated by Django 3.1.5 on 2021-01-05 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_cashier',
            field=models.BooleanField(default=False, verbose_name='is cashier'),
        ),
    ]
