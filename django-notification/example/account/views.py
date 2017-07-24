# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djangologout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from forms import RegisterForm, LoginForm, ChangePasswordForm, PrepareResetPasswordForm, ResetPasswordForm
from config import REGISTER_AUTO_LOGIN
from toollib.render import render_template
from toollib.email import send_html_template_email
from settings import DOMAIN, PROTOCOL, CONNECT_US


def register(request):
    redirect_url = reverse("account.views.home")
    if request.user.is_authenticated():
        return redirect(redirect_url)

    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            try:
                django_user = form.save()
                if REGISTER_AUTO_LOGIN:
                    django_user = authenticate(username=username, password=password)
                    djangologin(request, django_user)
                return redirect(redirect_url)
            except Exception, e:
                logging.error("failed to register: %s" % e)
                DjangoUser.objects.filter(username=username).delete()
    else:
        form = RegisterForm()

    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'注册'}]
    return render_template("register.html", request, form=form, breadcrumb=breadcrumb)


def login(request):
    next_url = request.GET.get("next", None)
    if next_url:
        redirect_url = next_url
    else:
        redirect_url = reverse("account.views.home")

    if request.user.is_authenticated():
        return redirect(redirect_url)

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            djangologin(request, form.get_user())
            return redirect(redirect_url)
    else:
        form = LoginForm()

    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'登录'}]
    return render_template("login.html", request, form=form, breadcrumb=breadcrumb)


def logout(request):
    djangologout(request)
    return redirect("/")


@login_required
def home(request):
    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'个人中心'}]
    return render_template("auth_userhome.html", request, use=request.user, breadcrumb=breadcrumb)


@login_required
def change_password(request):
    redirect_url = reverse("account.views.home")

    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(redirect_url)
    else:
        form = ChangePasswordForm(user=request.user)

    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'修改密码'}]
    return render_template("change_password.html", request, form=form, breadcrumb=breadcrumb)


def prepare_reset_password(request):
    statu = None
    msg = None
    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'忘记密码'}]

    if request.method == "POST":
        form = PrepareResetPasswordForm(request.POST)
        if form.is_valid():
            statu = "ok"
            msg = u"我们已经按你所提交的电子邮箱地址发送了密码设置说明.你应该很快就能收到这封邮件."
            django_user = DjangoUser.objects.filter(email=form.cleaned_data["email"])[0]
            token = default_token_generator.make_token(django_user)
            urllink = reverse("account.views.reset_password", args=(django_user.id, token, ))
            email_data = {"urllink": urllink, "user": django_user}
            email_data["domain"] = DOMAIN
            email_data["protocol"] = PROTOCOL
            email_data["connectus"] = CONNECT_US
            send_html_template_email(u"密码重置", "auth_email.html", email_data, [django_user.email], [])
    else:
        form = PrepareResetPasswordForm()

    return render_template("prepare_reset_password.html", request,
                           form=form, breadcrumb=breadcrumb, statu=statu, msg=msg)


def reset_password(request, userid, token):
    msg = ""
    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'重置密码'}]

    try:
        django_user = DjangoUser.objects.get(id=userid)
        if not default_token_generator.check_token(django_user, token):
            msg = u"参数错误!"
            form = ResetPasswordForm(user=django_user)
            return render_template("reset_password.html", request, breadcrumb=breadcrumb, msg=msg, form=form)
    except ObjectDoesNotExist:
        msg = u"该用户不存在!"
        form = ResetPasswordForm(user=None)
        return render_template("reset_password.html", request, breadcrumb=breadcrumb, msg=msg, form=form)

    if request.method == "POST":
        form = ResetPasswordForm(user=django_user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("account.views.login"))
    else:
        form = ResetPasswordForm(user=django_user)

    return render_template("reset_password.html", request, breadcrumb=breadcrumb, msg=msg, form=form)
