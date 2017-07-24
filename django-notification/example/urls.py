from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'index/', 'example.views.home'),                   
    url(r'notification/', include('notification.urls')),
    url(r'auth/', include('account.urls')),
    url(r'captcha/', include('captcha.urls')),
    url(r'^$', direct_to_template, {'template': 'example.html'}),
    url(r'^code/captcha/', include('captcha.urls')),
    url(r'code/image/(?P<key>\w+)/$','captcha.views.captcha_image',name='verificationcode-image'),
    url(r'code/new/key/$','toollib.verificationcode.code_new_key',name='verificationcode-new-key'),
)
