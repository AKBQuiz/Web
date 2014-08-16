from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','crawler.views.index', name="crawler"),
    url(r'^info/autorelation/','crawler.views.autorelation',name="crawler_autorelation"),
    url(r'^info/apply/','crawler.views.infoapply',name="crawler_infoapply"),
    url(r'^info/(\w+)/handler/','crawler.views.info',name="crawler_info_handler"),
    url(r'^info/(\w+)/$','crawler.views.infostart',name="crawler_info"),
    url(r'^schedule/','crawler.views.schedule',name="crawler_schedule"),
    url(r'^relation/unsolved/(\d+)-(\d+)/','crawler.views.relationunsolved',name="crawler_relationunsolved"),
    url(r'^relation/$','crawler.views.relation',name="crawler_relation"),
)
