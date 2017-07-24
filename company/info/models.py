#!/usr/bin/env python
#coding:UTF-8

from django.db import models

class CompanyInfo(models.Model):
    name = models.CharField(u"公司名称", max_length=50, )
    address =  models.TextField(u"公司地址", default="",)
    introduction = models.TextField(u"公司简介", default="",)
    telephone = models.CharField(u"公司电话", max_length=50, )
    mail = models.CharField(u"邮件地址", max_length=50, )
    qq = models.CharField(u"咨询qq", max_length=50, )
    class Meta:
        verbose_name = u"公司信息列表"

class Product(models.Model):
    name = models.CharField(u"产品名称", max_length=50, )
    introduction = models.TextField(u"产品简介", default="",)
    price = models.IntegerField(u"产品价格", default=0,)
    start_time = models.DateTimeField(u"开始时间")
    end_time = models.DateTimeField(u"结束时间", auto_now=False, default="")
    is_valid = models.IntegerField(u"是否有效", default=1,)
    class Meta:
        unique_together = ["name"]
        verbose_name = u"公司产品列表"

