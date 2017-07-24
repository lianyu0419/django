# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

def home(request):
    test = u"* test测试"
    
    return render_to_response("index.html", {"settings": settings, "request": request, "test": test},
                              context_instance=RequestContext(request))


def index(request, pageno=1):
    return render_to_response("index.html",
                              {"settings": settings, "request": request,
                               'prefix': '/index', 'pageno': pageno},
                              context_instance=RequestContext(request))


