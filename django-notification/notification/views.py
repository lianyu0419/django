#coding=utf-8

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
from notification.models import Notice, NoticeSetting, devices_set_true
from toollib.page import get_page
from toollib.render import render_template, render_json
from notification import config
from notification.forms import NoticeSettingForm
# from html5helper.utils import do_paginator
# from html5helper.decorator import render_template, render_json


@login_required
def home(request, page_no=1):
    notices = Notice.objects.filter(user=request.user)
    notices_page = get_page(notices, page_no, config.PAGE_SIZE)
    prefix = reverse("notification.views.home")
    
    current_nav = u"通知中心"
    breadcrumbs = [
        {"name": current_nav},
    ]
    return render_template("notification/home.html", request=request, prefix=prefix, \
                           notices_page=notices_page, breadcrumbs=breadcrumbs,
                           current_nav=current_nav)


@login_required
def change(request):
    notice_settings = NoticeSetting.objects.myself(request.user)
    
    if request.method == "POST":
        form = NoticeSettingForm(request.POST, user=request.user)
        if form.is_valid():
            for notice_setting in notice_settings:
                notice_setting.flags = devices_set_true(notice_setting.flags, form.cleaned_data[notice_setting.notice_type.label])
                notice_setting.save()
            messages.success(request, u"成功修改通知")
            
            return redirect(reverse("notification.views.change"))
    else:
        data = {}
        for notice_setting in notice_settings:
            data[notice_setting.notice_type.label] = notice_setting.devices_tuple()
        form = NoticeSettingForm(data, user=request.user)
    
    current_nav = u"设置"
    breadcrumbs = [
        {"name":u"通知中心", "url":reverse("notification.views.home")},
        {"name":current_nav},
    ]
    return render_template("notification/change.html", form=form, request=request, breadcrumbs=breadcrumbs, 
                           current_nav=current_nav)


@login_required
def go(request, notice_id):
    try:
        notice = Notice.objects.get(id = notice_id)
    except:
        messages.warning(request, u"该通知已经过期")
        return redirect(reverse("notification.views.home"))
    
    notice.is_read = True
    notice.save()
    return redirect(notice.target)


@login_required
@render_json
def my(request):
    reasons = []
    is_ok = False
    # check notifications
    notices = Notice.objects.unread_of_web(request.user)
    if len(notices) > 0:
        is_ok = True
        reasons += [mark_safe("<span class='text-muted'>%s</span> <a href='%s' target='_blank'>%s</a>" % (
                                    x.add_datetime,
                                    reverse("notification.views.go", args=[x.id]), 
                                    x.content)) for x in notices]
        
    return {"is_ok": is_ok, "reason": ".".join(reasons), "reasons": reasons}


@login_required
@render_json
def clear(request):
    # check notifications
    notices = Notice.objects.unread_of_web(request.user)
    for notice in notices:
        notice.is_read = True
        notice.save()
        
    return {"is_ok":True}
