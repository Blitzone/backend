from django.conf.urls import url

from .views import *
urlpatterns = [
	url(r'^register/$', RegisterView.as_view(), name='register'),
	url(r'^profile/$', ProfileView.as_view(), name='profile'),
	url(r'^verifyToken/$', 'rest_framework_jwt.views.verify_jwt_token'),
	url(r'^refreshToken/$', 'rest_framework_jwt.views.refresh_jwt_token'),
	url(r'^avatar/$', AvatarView.as_view(), name='avatar'),
	url(r'^changeUsername/$', ChangeUsernameView.as_view(), name='changeUsername'),
	url(r'^changePassword/$', ChangePasswordView.as_view(), name='changePassword'),
	url(r'^searchUser/$', SearchUserView.as_view(), name='searchUser'),
	url(r'^addFollow/$', AddFollowView.as_view(), name='addFollow'),
	url(r'^delFollow/$', DelFollowView.as_view(), name='delFollow'),
]
