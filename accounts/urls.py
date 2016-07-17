from django.conf.urls import url
from rest_framework.authtoken import views

from .views import *
urlpatterns = [
	url(r'^register/$', RegisterView.as_view(), name='register'),
	url(r'^profile/$', ProfileView.as_view(), name='profile'),
	url(r'^login/$',views.obtain_auth_token),
	url(r'^verifyToken/$', VerifyTokenView.as_view(), name='verifyToken'),
	url(r'^avatar/$', AvatarView.as_view(), name='avatar'),
	url(r'^changeUsername/$', ChangeUsernameView.as_view(), name='changeUsername'),
	url(r'^changePassword/$', ChangePasswordView.as_view(), name='changePassword'),
	url(r'^searchUser/$', SearchUserView.as_view(), name='searchUser'),
	url(r'^addFollow/$', AddFollowView.as_view(), name='addFollow'),
	url(r'^delFollow/$', DelFollowView.as_view(), name='delFollow'),
	url(r'^getFollowing/$', GetFollowingView.as_view(), name='getFollowing'),
	url(r'^getFollowers/$', GetFollowersView.as_view(), name='getFollowers'),

]
