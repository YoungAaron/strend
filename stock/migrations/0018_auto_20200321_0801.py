# Generated by Django 2.2 on 2020-03-21 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0017_fundlist_fundportfolio_margin_pledgestat_sharefloat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundlist',
            name='name',
            field=models.CharField(max_length=100, verbose_name='简称'),
        ),
        migrations.AlterField(
            model_name='fundlist',
            name='trustee',
            field=models.CharField(max_length=100, verbose_name='受托人'),
        ),
    ]
