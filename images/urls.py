from django.conf.urls import url

from .views import TopicView, ChaptersView, UploadUserChapterView, GetUserChaptersView
urlpatterns = [
    url(r'^topic/$', TopicView.as_view(), name='topic'),
    url(r'^chapters/$', ChaptersView.as_view(), name='chapters'),
    url(r'^uploadUserChapter/$', UploadUserChapterView.as_view(), name='uploadUserChapter'),
    url(r'^getUserChapters/$', GetUserChaptersView.as_view(), name='getUserChapters'),
]
