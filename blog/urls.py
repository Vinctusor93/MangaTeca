from django.urls import path
from . import views
import logging
urlpatterns = [  
    path('manga/addManga/', views.addManga, name='addManga'),
    path('manga/new/', views.manga_new, name='manga_new'),
    path('manga/newTag', views.newTag, name='newTag'),
    path('manga/tableMangaFilter', views.tableMangaFilter, name='tableMangaFilter'),
    path('manga/<str:title>/', views.manga_detail, name='manga_detail'),
    path('manga/<str:title>/edit/', views.manga_edit, name='manga_edit'),
    path('', views.post_list, name='post_list'),
    
]
logger = logging.getLogger("Logger")
logger.warning(urlpatterns)