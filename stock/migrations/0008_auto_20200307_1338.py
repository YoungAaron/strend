# Generated by Django 2.2 on 2020-03-07 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0007_indexlist_fun_one'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexlist',
            name='fun_two',
            field=models.CharField(default=0, max_length=1, verbose_name='行业对比'),
        ),
        migrations.AlterField(
            model_name='indexlist',
            name='fun_one',
            field=models.CharField(default=0, max_length=1, verbose_name='市场对比'),
        ),
    ]
