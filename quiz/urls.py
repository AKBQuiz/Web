from django.conf.urls import patterns, include, url
from quiz import views

urlpatterns = patterns('',
    url(r'^$',views.quizgame, name="quizgame"),
    url(r'^collect/$',views.collect,name="quiz_collect"),
    url(r'^collect/query/$',views.query,name="quiz_query"),

    # APIs
    url(r'^api/getquiz/$',views.api_quiz_get,name="api_quiz_get"),
    url(r'^api/collect/$',views.api_quiz_submit,name="api_quiz_submit"),
    url(r'^api/comment/$',views.api_quiz_comment,name="api_quiz_comment"),
)
