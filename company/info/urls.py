from django.conf.urls import patterns, include, url

urlpatterns = patterns('info.views',

    url(r'^product/(?P<product_id>(\d+))', "list_product_content", name="list_product_content"),

)

