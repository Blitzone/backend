from django.conf.urls import url

from .views import TopicView, ChaptersView, UserChapterView
urlpatterns = [
    url(r'^topic/$', TopicView.as_view(), name='topic'),
    url(r'^chapters/$', ChaptersView.as_view(), name='chapters'),
    url(r'^userChapter/$', UserChapterView.as_view(), name='userChapter'),
]
