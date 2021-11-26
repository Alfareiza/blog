from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # Listar todos os posts
    path('', views.post_list, name='post_list'),
    # Listar posts baseado num tag
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    # Detalhe de uma view
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # Compartilhar view
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    # Pág 107
    path('feed/', LatestPostsFeed(), name='post_feed'),

]
