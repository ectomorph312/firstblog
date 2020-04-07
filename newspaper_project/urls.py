from django.contrib import admin
from django.urls import path, include 
from django.conf.urls import url



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('articles/', include('articles.urls')),
    path('', include('pages.urls')),
    # url(r'^api/v1/', include(apipatterns, namespace='api')),
]