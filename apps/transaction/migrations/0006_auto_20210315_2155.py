# Generated by Django 3.1.6 on 2021-03-15 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0005_auto_20210315_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
