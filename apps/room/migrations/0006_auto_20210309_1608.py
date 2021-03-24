# Generated by Django 3.1.6 on 2021-03-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0005_auto_20210227_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='userBanker',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='limit',
            field=models.IntegerField(default='5'),
        ),
    ]