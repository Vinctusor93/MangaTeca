from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('manga/new/', views.manga_new, name='manga_new'),
    path('manga/newTag', views.newTag, name='newTag'),
    path('manga/tableMangaFilter', views.tableMangaFilter, name='tableMangaFilter'),
    path('manga/<str:title>/', views.manga_detail, name='manga_detail'),
    path('manga/<str:title>/edit/', views.manga_edit, name='manga_edit'),
]
