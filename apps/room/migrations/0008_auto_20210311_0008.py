# Generated by Django 3.1.6 on 2021-03-11 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0007_auto_20210309_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='limit',
            field=models.IntegerField(default='0'),
        ),
    ]
