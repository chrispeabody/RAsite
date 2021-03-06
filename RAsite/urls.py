"""RAsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from RAsite import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^about/$', views.about),
    #url(r'^blogapp/', include('blogapp.urls')),
    url(r'^registerForm/$', views.registerForm),
    url(r'^registerUser/$', views.registerUser),
    url(r'^logout/$', views.loggingout),
    url(r'^loginForm/$', views.logginginForm),
    url(r'^login/$', views.loggingin),
    url(r'^aggReviews/$', views.aggReviews),
    url(r'^addReview/$', views.addReview),
    #url(r'^montyhall/$', views.montyhall),
    #url(r'^runbayesnet/$', views.runbayesnet),
    url(r'^getScore/$', views.getScore),
    url(r'^initTables/$', views.initTables),
    url(r'^results/$', views.results),
    url(r'^tutorial/$', views.tutorial)
]
