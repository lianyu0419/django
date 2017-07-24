#!/usr/bin/env python
#coding:UTF-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from info.models import CompanyInfo,Product
from django.template import RequestContext
from render import render_template

def home_page(request):
    company_info = CompanyInfo.objects.get(id=1)
    products = Product.objects.filter(is_valid=1).values("name","id")
    return render_template("home_page.html", **locals())

def list_product_content(request, product_id):
    company_info = CompanyInfo.objects.get(id=1)
    products = Product.objects.filter(is_valid=1).values("name","id")
    product_info = Product.objects.get(is_valid=1,id=product_id)
    return render_template("product_page.html", **locals())