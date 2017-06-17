from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^new$', views.newblog),
	url(r'^SubmitNewBlog/$', views.getNewBlogData),
	url(r'^registerForm/$', views.registerForm),
	url(r'^registerUser/$', views.registerUser),
	url(r'^logout/$', views.loggingout),
	url(r'^loginForm/$', views.logginginForm),
	url(r'^login/$', views.loggingin),
]