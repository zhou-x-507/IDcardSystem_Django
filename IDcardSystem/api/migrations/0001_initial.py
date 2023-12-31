# Generated by Django 4.2.3 on 2023-07-29 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='城市')),
            ],
        ),
        migrations.CreateModel(
            name='Ethnics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='民族')),
            ],
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='省份')),
            ],
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=18, verbose_name='身份证号')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('sex', models.IntegerField(choices=[(0, '女'), (1, '男')], verbose_name='性别')),
                ('birthday', models.DateField(max_length=100, verbose_name='生日')),
                ('address', models.CharField(max_length=100, verbose_name='详细地址')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cities', verbose_name='城市')),
                ('ethnic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ethnics', verbose_name='民族')),
            ],
        ),
        migrations.AddField(
            model_name='cities',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.provinces'),
        ),
    ]
