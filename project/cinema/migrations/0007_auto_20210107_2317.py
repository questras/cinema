# Generated by Django 3.1.5 on 2021-01-07 22:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_auto_20210107_2315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='showing',
            name='id',
        ),
        migrations.AlterField(
            model_name='showing',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
