from django.contrib import admin
from .models import PostManga
from .models import Tag


admin.site.register(PostManga)
admin.site.register(Tag)
