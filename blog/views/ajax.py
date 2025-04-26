import logging
import random
import re
import bs4
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
import requests
from ..forms.newMangaForm import NewMangaForm
from ..models import PostManga,Tag
from members.models import CustomUser
import ast
logger = logging.getLogger("Logger")

@login_required
def searchManga(request):
    logger.warning("searchManga")
    search = request.POST.get("searchWord")
    #mangaFound = request.POST.get("elementsResult")
    #logger.warning(mangaFound)
    #if search == '':
    #    resultsAllManga = None
    #else:
    resultsManga = PostManga.objects.filter(title__istartswith=search)
    user = request.user
    userManga = user.mangaUser.all()
    logger.warning("eccomi "+str(userManga))
    #resultsManga = resultsAllManga.difference(userManga)
    logger.warning("searchManga+1")
    return render(request, 'blog/tableMangaSearch.html', {'Mangalist': resultsManga,"myManga":userManga})

@login_required
def insertManga(request):
    logger.warning("insertManga")
    choice = request.POST.get("choice")
    id = request.POST.get("id")
    manga= PostManga.objects.get(id=id)
    user = request.user
    user.mangaUser.add(manga) 
    if choice == "Favorite":
        logger.warning("eccomi in list")
        user.favoriteMangaUser.add(manga)        
    user.save()
    result = searchManga(request)
    return result


    
def tableMangaFilter(request):
    logger.warning("filterTag")
    statusList = ["In corso", "Completato", "Lasciato momentaneamente"]
    filterTags = request.POST.get("filterTag")
    statusState = request.POST.get("status")
    filterTags = ast.literal_eval(filterTags)
    logger.warning(filterTags)
    logger.warning(statusState)
    user =request.user
    
    resultManga = user.mangaUser.all()
    for elem in filterTags:

        logger.warning(elem)
        resultManga = resultManga.filter(tags=elem)
    if statusState in statusList:
        resultManga = resultManga.filter(status=statusState)

    return render(request, 'blog/tableManga.html', {'Mangalist': resultManga})

# Create your views here.
def newTag(request):
    logger.warning("newTag")
    newTag = request.POST.get("newTag")
  #  logger.warning(newTag)
    tag = Tag.objects.filter(tag=newTag).count()
    json = {}
    if(tag != 0):
        logger.warning("Tag esistente")
        json["message"]= "Tag già esistente"
    else:
        items = ["primary","secondary","success","danger","warning","info","dark"]
        color = random.choice(items)
        logger.warning("Tag nuovo")
        json["message"] = "Tag nuovo"
        Tag.objects.create(tag=newTag,color=color)
   # logger.warning(json)
    return  JsonResponse(json)

def manageFavorite(request):
    choice = request.POST.get("choice")
    id = request.POST.get("id")
    logger.warning(id)
    manga = PostManga.objects.get(id=id)
    user = request.user
    if choice == "addFavorite":
        user.favoriteMangaUser.add(manga) 
    else:
        user.favoriteMangaUser.remove(manga)
    json = {}
    
    return  JsonResponse(json) 