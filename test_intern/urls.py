"""test_intern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from test_intern import view

urlpatterns = [
   url(r'^admin/', include(admin.site.urls)),
    url(r'^$', view.get_data),#http://cs.sehir.edu.tr/courserecommender/

    url(r'^Result/$', view.get_recommendations), #http://cs.sehir.edu.tr/courserecommender/Result/
    url(r'^login/$', view.login_user),#http://cs.sehir.edu.tr/courserecommender/login/
    url(r'^usersaved/$', view.UserSaved),#http://cs.sehir.edu.tr/courserecommender/usersaved/

     url(r'^admin_tools/$', view.my_view),#http://cs.sehir.edu.tr/courserecommender/admin_tools/
    url(r'^login/$', view.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth'))





]
