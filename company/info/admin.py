#!/usr/bin/env python
#coding:UTF-8
from django.contrib import admin
from info.models import CompanyInfo, Product

class CompanyInfoAdmin(admin.ModelAdmin):
    """docstring for AuthorAdmin"""
    list_display = ('name', 'address', 'introduction', 'telephone', 'qq', 'mail')
admin.site.register(CompanyInfo, CompanyInfoAdmin)

class ProductAdmin(admin.ModelAdmin):
    """docstring for AuthorAdmin"""
    list_display = ('name', 'introduction', 'price', 'start_time', 'end_time', 'is_valid')
admin.site.register(Product, ProductAdmin)