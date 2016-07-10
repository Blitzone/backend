from django.conf.urls import url

from .views import *
urlpatterns = [
    url(r'^topic/$', TopicView.as_view(), name='topic'),
    url(r'^chapters/$', ChaptersView.as_view(), name='chapters'),
    url(r'^uploadUserChapter/$', UploadUserChapterView.as_view(), name='uploadUserChapter'),
    url(r'^getUserChapters/$', GetUserChaptersView.as_view(), name='getUserChapters'),
    url(r'^searchPhotoChapters/$', SearchPhotoChapterView.as_view(), name='searchPhotoChapters'),
    url(r'^daily/$', DailyPhotoChapterView.as_view(), name='daily'),
    url(r'^likeTopic/$', LikeTopicView.as_view(), name='likeTopic'),
    url(r'^unlikeTopic/$', UnLikeTopicView.as_view(), name='unlikeTopic'),
    url(r'^dislikeTopic/$', DisLikeTopicView.as_view(), name='dislikeTopic'),
    url(r'^undislikeTopic/$', UnDisLikeTopicView.as_view(), name='undislikeTopic'),
    url(r'^sendBlitz/$', SendBlitzView.as_view(), name='sendBlitz'),
]
