from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from blog.models import PostManga

class CustomUser(AbstractUser):
    mangaUser = models.ManyToManyField(PostManga,blank=True,related_name="userManga")
    favoriteMangaUser = models.ManyToManyField(PostManga,blank=True,related_name="favoriteManga")
