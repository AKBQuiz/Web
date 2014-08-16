from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #url(r'election/$',               'charts.views.election', name='election_chart'),
    url(r'election/single/(\d{2,3})/',     'charts.views.election_single', ),
    url(r'election/group/(\w{3,4}\d{2})/', 'charts.views.election_group', ),
    url(r'election/map/(\d{2,3})/',        'charts.views.election_map', ),
    url(r'election/trend/(\w+)/',          'charts.views.election_trend', ),
    url(r'election/rank/(\d{2,3})',        'charts.views.election_rank', ),
)