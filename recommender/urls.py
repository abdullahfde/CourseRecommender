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
from recommender import view

urlpatterns = [
    url(r'^courserecommender/admin/', include(admin.site.urls)),
    url(r'^courserecommender/$', view.get_data),  # http://cs.sehir.edu.tr/courserecommender/
    url(r'^courserecommender/result/$', view.get_recommendations, name="result"),
    url(r'^courserecommender/login/$', view.login_user, name="admin-login"),
    url(r'^courserecommender/usersaved/$', view.UserSaved, name="usersaved"),
    url(r'^courserecommender/admin-tools/$', view.my_view, name="admin-tools"),
    url('courserecommender/', include('social.apps.django_app.urls', namespace='social')),
    url('courserecommender/', include('django.contrib.auth.urls', namespace='auth'))

]
