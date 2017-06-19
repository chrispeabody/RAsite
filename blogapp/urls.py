from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^new$', views.newblog),
	url(r'^SubmitNewBlog/$', views.getNewBlogData),
]