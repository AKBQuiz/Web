from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$'  ,'memberinfo.views.index' , name='database'),
    url(r'^grouplist/'                                   ,'memberinfo.views.grouplist'),

    url(ur'^group_(\w+)/team_([a-zA-Z48]+|\u7814\u7a76\u751f)/memberlist/' ,'memberinfo.views.group_team_memberlist'),
    url(ur'^group_(\w+)/team_([a-zA-Z48]+|\u7814\u7a76\u751f)/'            ,'memberinfo.views.group_team'       , name='team'),
    url( r'^group_(\w+)/memberlist/'                   ,'memberinfo.views.group_memberlist'),
    url( r'^group_(\w+)/teamlist/'                     ,'memberinfo.views.group_teamlist'),
    url( r'^group_(\w+)/'                              ,'memberinfo.views.group'            , name='group'),

    url( r'^member_(\d+)/avatar/$'                     ,'memberinfo.views.avatar', name='avatar'),
    url( r'^member_(\d+)/$'                            ,'memberinfo.views.member', name='member'),
    url(ur'^name/([\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+)/$','memberinfo.views.name', name='name'),

    url( r'^birthday/year/(\d{4})/$'                    ,'memberinfo.views.birthday_year', name='birthday_year'),
    url( r'^birthday/date/(\d{1,2})/(\d{1,2})/span/(\d{1,3})/$','memberinfo.views.birthday_date_span',name='birthday_date_span'),
    url( r'^birthday/date/(\d{1,2})/(\d{1,2})/to/(\d{1,2})/(\d{1,2})/$','memberinfo.views.birthday_date_range',name='birthday_date_range'),
    url( r'^birthday/date/(\d{1,2})/(\d{1,2})/$'        ,'memberinfo.views.birthday_date', name='birthday_date'),
    url( r'^birthday/month/(\d{1,2})/$'                 ,'memberinfo.views.birthday_month',name='birthday_month'),
    url( r'^birthday/day/(\d{1,2})/$'                   ,'memberinfo.views.birthday_day',  name='birthday_day'),
    url( r'^birthday/weekday/(\d{1,2})/$'               ,'memberinfo.views.birthday_weekday',name='birthday_weekday'),
    url( r'^birthday/(\d{4})/(\d{1,2})/(\d{1,2})/span/(\d)/$','memberinfo.views.birthday_span',name='birthday_span'),
    url( r'^birthday/(\d{4})/(\d{1,2})/(\d{1,2})/to/(\d{4})/(\d{1,2})/(\d{1,2})/$','memberinfo.views.birthday_range',name='birthday_range'),
    url( r'^birthday/(\d{4})/(\d{1,2})/(\d{1,2})/$'     ,'memberinfo.views.birthday',      name='birthday'),

    url( r'^hometown/([a-zA-Z]+)/$'                     ,'memberinfo.views.hometown_name', name='hometown_name'),
    url( r'^hometown/(\d+)/$'                           ,'memberinfo.views.hometown_id',   name='hometown_id'),
    url( r'^generation/(\w+)/([0-9.]{1,3})/$'           ,'memberinfo.views.generation',    name='generation'),
)
