# Generated by Django 4.2.3 on 2023-07-20 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ethnics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ethnic', models.CharField(max_length=100, verbose_name='民族')),
            ],
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=18, verbose_name='身份证号')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(0, '女'), (1, '男')], verbose_name='性别')),
                ('ethnic', models.CharField(max_length=10, verbose_name='民族')),
                ('birthday', models.DateField(max_length=100, verbose_name='生日')),
                ('province', models.CharField(max_length=100, verbose_name='省')),
                ('city', models.CharField(max_length=100, verbose_name='市')),
                ('address', models.CharField(max_length=100, verbose_name='详细地址')),
            ],
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=100, verbose_name='省')),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='市')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.provinces')),
            ],
        ),
    ]
