# Generated by Django 2.2 on 2020-03-21 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0018_auto_20200321_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundlist',
            name='ftype',
            field=models.CharField(max_length=100, verbose_name='基金类型'),
        ),
    ]
