from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import PostSearchAPIView

urlpatterns =[
    path('', views.PostList.as_view()),
    path('detail/<int:pk>/', views.PostDetail.as_view()),
    path('write/', views.PostWrite.as_view()),
    path('search/', PostSearchAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)