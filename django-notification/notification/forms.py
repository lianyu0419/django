#coding=utf-8
  
from django import forms
# from html5helper.forms import BasisForm
# from html5helper.fields import ChoiceField
# from html5helper.widgets import InlineCheckboxSelectMultiple
from notification.models import NoticeSetting
 
from django.forms.util import ErrorList
from django import forms
from django.utils.safestring import mark_safe


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u""
        return u'<div class="alert">%s</div>' % ''.join([u'<div class="alert-error">%s</div>' % e for e in self])

    def as_ul(self):
        return self.as_divs()


class BasisForm(forms.Form):
    """ basis form class.
    """
    _custom_error = ""
    _success_tips = ""

    @property
    def custom_error(self):
        if self._custom_error == "":
            return ""
        return mark_safe(u"<div class=\"alert\">%s</div>" % self._custom_error)

    def set_custom_error(self, msg):
        self._custom_error = msg

    @property
    def success_tips(self):
        if self._success_tips == "":
            return ""
        return mark_safe(u"<div class=\"alert alert-success\">%s</div>" % self._success_tips)

    def set_success_tips(self, tips):
        self._success_tips = tips


class NoticeSettingForm(BasisForm):
    def __init__(self, *args, **kwargs):
        """ must have "user" as args
        """
        self.user = None
        if "user" in kwargs:
            self.user = kwargs.pop("user")
         
        super(NoticeSettingForm, self).__init__(*args, **kwargs)
         
        notice_settings = NoticeSetting.objects.myself(self.user)
        for notice_setting in notice_settings:
            self.fields[notice_setting.notice_type.label] = forms.MultipleChoiceField(label=notice_setting.notice_type.display,
                                                                         help_text=notice_setting.notice_type.description,
                                                                         widget=forms.CheckboxSelectMultiple(), 
                                                                         choices=NoticeSetting.DEVICE_CHOICES, 
                                                                         required=False)
# class NoticeSettingForm(BasisForm):
#     monitor_deading = forms.MultipleChoiceField(label=u"监控快过期", choices=NoticeSetting.DEVICE_CHOICES,
#                                                 widget=forms.CheckboxSelectMultiple(), help_text=u"当监控快过期时，通知我")
#     monitor_deaded = forms.MultipleChoiceField(label=u"监控过期", choices=NoticeSetting.DEVICE_CHOICES,
#                                                 widget=forms.CheckboxSelectMultiple(), help_text=u"当监控过期时，通知我")
#     pre_notify_days = forms.IntegerField(label=u"提前几天通知", help_text=u"提前通知时间")
# 
#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop("user", None)
#         super(NoticeSetting, self).__init__(*args, **kwargs)
#         notification_control = NoticeSetting.user_self_sets(self.user)
#         self.fields["monitor_deading"].initial = (NoticeSetting.notice_devices_tuple(notification_control.monitor_deading))
#         self.fields["monitor_deaded"].initial = NoticeSetting.notice_devices_tuple(notification_control.monitor_deaded)
#         self.fields["pre_notify_days"].initial = notification_control.pre_notify_days
