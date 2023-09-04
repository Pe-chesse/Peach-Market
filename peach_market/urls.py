"""
URL configuration for peach_market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from chat.consumers import ChatConsumer

API_VERSIONS = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{API_VERSIONS}post/', include('post.urls')),
    path(f'{API_VERSIONS}account/',include('user.urls')),
    path(f'{API_VERSIONS}chat/', include('chat.urls')),
    path(f'{API_VERSIONS}bucket/', include('bucket.urls')),
]
