# Generated by Django 3.1.6 on 2021-03-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210227_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default=None, max_length=15, unique=True),
        ),
    ]