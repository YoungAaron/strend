# Generated by Django 2.2 on 2020-03-21 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0019_auto_20200321_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundlist',
            name='benchmark',
            field=models.CharField(max_length=300, verbose_name='业绩比较基准'),
        ),
        migrations.AlterField(
            model_name='fundlist',
            name='ftype',
            field=models.CharField(max_length=40, verbose_name='基金类型'),
        ),
        migrations.AlterField(
            model_name='fundlist',
            name='trustee',
            field=models.CharField(max_length=50, verbose_name='受托人'),
        ),
    ]
