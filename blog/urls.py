from django.urls import path
#from . import views
from blog.views import views,ajax
import logging
urlpatterns = [
    path('', views.post_list, name='post_list'),  
    path('manga/rest/searchManga/', ajax.searchManga, name='searchManga'),
    path('manga/rest/new/', views.manga_new, name='manga_new'),
    path('manga/userlist/All', views.user_list, name='user_list'),
    path('manga/<str:type>', views.post_list, name='favorite_list'),
    path('manga/rest/insertManga/', ajax.insertManga, name='insertManga'),
    path('manga/rest/newTag', ajax.newTag, name='newTag'),
    path('manga/rest/manageFavorite', ajax.manageFavorite, name='manageFavorite'),
    path('manga/rest/tableMangaFilter', ajax.tableMangaFilter, name='tableMangaFilter'),
    path('manga/<str:title>/edit/', views.manga_edit, name='manga_edit'),
    path('manga/addManga/', views.addManga, name='addManga'),
    path('manga/<str:title>/detail/', views.manga_detail, name='manga_detail'),
]
