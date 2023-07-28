from django.db import models
from django.contrib.auth.models import AbstractUser


class Persons(models.Model):
    number = models.CharField(max_length=18, verbose_name='身份证号')  # 身份证号码
    name = models.CharField(max_length=50, verbose_name='姓名')  # 姓名
    sex_choices = ((0, '女'), (1, '男'))  # 性别
    sex = models.IntegerField(choices=sex_choices, verbose_name='性别')
    # ethnic = models.CharField(max_length=10, verbose_name='民族')  # 民族
    ethnic = models.ForeignKey('Ethnics', on_delete=models.CASCADE, verbose_name='民族')  # 外键，一对多
    birthday = models.DateField(max_length=100, verbose_name='生日')  # 生日
    # province = models.CharField(max_length=100, verbose_name='省份')  # 省份
    province = models.ForeignKey('Provinces', on_delete=models.CASCADE, verbose_name='省份')  # 外键，一对多
    # city = models.CharField(max_length=100, verbose_name='城市')  # 城市
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, verbose_name='城市')  # 外键，一对多
    address = models.CharField(max_length=100, verbose_name='详细地址')  # 详细地址


class Provinces(models.Model):
    province = models.CharField(max_length=100, verbose_name='省份')  # 省份


class Cities(models.Model):
    city = models.CharField(max_length=100, verbose_name='城市')  # 城市
    province = models.ForeignKey('Provinces', on_delete=models.CASCADE)  # 外键


class Ethnics(models.Model):
    ethnic = models.CharField(max_length=100, verbose_name='民族')  # 民族



