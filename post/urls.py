from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns =[
    # 글 목록 조회
    path('', views.PostList.as_view()),
    # 글 상세 조회
    path('detail/<int:pk>/', views.PostDetail.as_view()),
    # 글 작성
    path('write/', views.PostWrite.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)