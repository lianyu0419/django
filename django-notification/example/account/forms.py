# -*- coding: utf-8 -*-
""" user related forms """

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User as DjangoUser

from config import EMAIL_SUFFIX, PASSWORD_MIN_LENGTH


class RegisterForm(UserCreationForm):
    class Meta:
        fields = ("username", "email",)
        model = DjangoUser

    def clean_email(self):
        email = self.cleaned_data["email"]

        if DjangoUser.objects.filter(email=email).count():
            raise forms.ValidationError(u"该邮箱已经被注册!")

        if EMAIL_SUFFIX and not email.endswith(EMAIL_SUFFIX):
            raise forms.ValidationError(u"邮箱域名必须是%s!" % EMAIL_SUFFIX)

        return email

    def clean_password1(self):
        return do_check_password_length(self, 'password1')


class LoginForm(AuthenticationForm):
    pass


class ChangePasswordForm(PasswordChangeForm):
    def clean_new_password1(self):
        return do_check_password_length(self, 'new_password1')


class PrepareResetPasswordForm(forms.Form):
    email = forms.EmailField(required=True, label=u'注册邮箱')

    def clean_email(self):
        email = self.cleaned_data["email"]
        if DjangoUser.objects.filter(email=email).count() < 1:
            raise forms.ValidationError(u"该邮箱未注册!")
        return email


class ResetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        return do_check_password_length(self, 'new_password1')


def do_check_password_length(form, password_key):
    password = form.cleaned_data.get(password_key)
    if len(str(password).strip()) < PASSWORD_MIN_LENGTH:
        raise forms.ValidationError(u"至少 %s 位密码!" % PASSWORD_MIN_LENGTH)
    return password
