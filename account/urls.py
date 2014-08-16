from django.conf.urls import patterns, include, url
from account import views

urlpatterns = patterns('',
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$',    views.login, name='login'),
    url(r'^logout/$',   'django.contrib.auth.views.logout', {'template_name': 'logout.html'},name='logout'),

    url(r'^password-reset/$',
        'django.contrib.auth.views.password_reset', 
        {'template_name': 'password-reset.html'},
        name='password_reset'
    ),
    url(r'^password-reset-done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'password-reset-done.html'},
        name='password_reset_done'
    ),
    url(r'^password-reset-confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        views.password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(r'^password-reset-complete/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'password-reset-complete.html'},
        name='password_reset_complete'
    ),

    url(r'^password-change/$',
        views.password_change,
        name='password_change'
    ),
    url(r'^password-change-done/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'password-change-done.html'},
        name='password_change_done'
    ),

    url(r'^profile/$',      views.info,     name='userinfo'),
    url(r'^profile/edit/$', views.editinfo, name='userinfo_edit'),

    url(r'^snslogin/(\w+)/$',views.sns_signin, name='sns_signin'),
    url(r'^snscallback/(\w+)/$',views.sns_callback, name='sns_callback'),

    url(r'^sns-notsupport/$',views.sns_notsupport, name='sns_notsupport'),

    # for test
    url(r'^snsreg-success/$',views.snsreg_success ),

)