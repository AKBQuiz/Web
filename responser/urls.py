from django.conf.urls import patterns, include, url
from responser import views

urlpatterns = patterns('',
    url(r'^weixin/test/$',views.weixin,{"istest":True},name="weixin_responser"),
    url(r'^weixin/$',views.weixin,name="weixin_responser"),
)