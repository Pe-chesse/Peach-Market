from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns =[
    # <Post - 게시글>
    # 게시글 목록 조회
    path('', views.PostList.as_view()),
    # 게시글 작성
    path('write/', views.PostWrite.as_view()),
    # 게시글 상세 조회
    path('detail/<int:pk>/', views.PostDetail.as_view()),
    # 게시글 수정
    path('detail/<int:pk>/edit/', views.PostUpdate.as_view()),
    # 게시글 삭제
    path('detail/<int:pk>/delete/', views.PostDelete.as_view()),
    
    # <Product - 상품>
    # 상품 목록 조회
    path('product/', views.ProductList.as_view()),
    # 상품 등록
    path('product/write/', views.ProductWrite.as_view()),
    # 상품 상세 조회
    path('product/detail/<int:pk>/', views.ProductDetail.as_view()),
    # 상품 수정
    path('product/detail/<int:pk>/edit/', views.ProductUpdate.as_view()),
    # 상품 삭제
    path('product/detail/<int:pk>/delete/', views.ProductDelete.as_view()),
    
    # <Comment - 댓글>
    path('detail/<int:post_id>/comment/', views.CommentView.as_view()),
    path('detail/<int:post_id>/comment/<int:comment_id>', views.CommentDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)