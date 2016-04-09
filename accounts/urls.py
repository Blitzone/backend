from django.conf.urls import url

from .views import RegisterView, AvatarView, ProfileView
urlpatterns = [
	url(r'^register/$', RegisterView.as_view(), name='register'),
	url(r'^profile/$', ProfileView.as_view(), name='profile'),
	url(r'^verifyToken/$', 'rest_framework_jwt.views.verify_jwt_token'),
	url(r'^refreshToken/$', 'rest_framework_jwt.views.refresh_jwt_token'),
	url(r'^avatar/$', AvatarView.as_view(), name='avatar'),
]
