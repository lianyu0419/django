# -*- coding:utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape


__all__ = ('BaseForm', 'Form',)


class BaseForm(forms.BaseForm):
    pass


@python_2_unicode_compatible
class BootstrapErrorList(ErrorList):
    def as_ul(self):
        if not self: return u''
        return mark_safe(u'<ul class="errorlist">%s</ul>'
                % ''.join([u'<li><small><font color="#ff0000">%s</font></small></li>' %
                           conditional_escape(force_unicode(e)) for e in self]))


    def __str__(self):
        return self.as_ul()


class Form(forms.Form):
    def __init__(self, *args, **kwargs):
        new_kwargs = {'error_class': BootstrapErrorList}
        new_kwargs.update(kwargs)
        super(Form, self).__init__(*args, **new_kwargs)
