# Generated by Django 3.1.6 on 2021-03-15 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0003_auto_20210315_0101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='idTransaction',
        ),
        migrations.AddField(
            model_name='transaction',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
