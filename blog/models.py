import logging

from django.conf import settings
from django.db import models
from django.utils import timezone
import re
class Tag(models.Model):
    tag = models.CharField(max_length=100, primary_key=True)
    color = models.CharField(max_length=100)

    def getTagAsattributeClassHtml(self):
            return self.tag.replace(" ","-")

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['tag']

class PostManga(models.Model):
    STATUS_MANGA = [
        ("In corso","In corso"),
        ("Completato","Completato"),
        ("Lasciato momentaneamente","Lasciato momentaneamente"),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=400,unique=True)
    lastChapter = models.CharField(max_length=100)
    dateLastChapter = models.CharField(max_length=20)
    author = models.CharField(max_length=150,blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=150, choices=STATUS_MANGA, default="In corso")
    date_created = models.DateField(auto_now=True)
    urlImage = models.URLField(max_length=300)
    tags = models.ManyToManyField(Tag,blank=True,null=True)
    image = models.FileField(null=True,blank=True,upload_to="images/manga/")

    def getUrlManga(self):
        txt = self.title
        txt = re.sub('[^A-Za-z0-9-\s]+', '', txt)
        x = txt.lower()
        x = x.replace(" ", "-")
        x = re.sub('-+', '-', x)
        logging.warning("https://www.mangabats.com/manga/" + x)
        return "https://www.mangabats.com/manga/" + x

    def __str__(self):
        return self.title

