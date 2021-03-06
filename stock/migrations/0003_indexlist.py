# Generated by Django 2.2 on 2020-02-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20200229_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ts_code', models.CharField(max_length=9, verbose_name='TS代码')),
                ('name', models.CharField(max_length=30, verbose_name='简称')),
                ('fullname', models.CharField(max_length=50, verbose_name='指数全称')),
                ('market', models.CharField(max_length=10, verbose_name='市场')),
                ('publisher', models.CharField(max_length=10, verbose_name='发布方')),
                ('index_type', models.CharField(max_length=100, verbose_name='指数风格')),
                ('category', models.CharField(max_length=50, verbose_name='指数类别')),
                ('base_date', models.CharField(max_length=8, verbose_name='基期')),
                ('base_point', models.FloatField(verbose_name='基点')),
                ('list_date', models.CharField(max_length=8, verbose_name='发布日期')),
                ('weight_rule', models.CharField(max_length=50, verbose_name='加权方式')),
                ('desc', models.CharField(max_length=500, verbose_name='描述')),
                ('exp_date', models.CharField(max_length=8, verbose_name='终止日期')),
            ],
            options={
                'db_table': 'index_list',
            },
        ),
    ]
