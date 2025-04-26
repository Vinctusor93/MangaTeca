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
from ..models import PostManga
from ..models import Tag
from members.models import CustomUser
import ast
logger = logging.getLogger("Logger")
from blog.views import ajax

@login_required
def post_list(request,type=None):
    logger.warning("post_list")
    favoriteManga = PostManga.objects.none
    user = request.user
    if type == "Favorite":
        mangas = user.favoriteMangaUser.all() #PostManga.objects.all()
    else:
        mangas = user.mangaUser.all() #PostManga.objects.all()
        favoriteManga = user.favoriteMangaUser.all()
    
    tags = Tag.objects.filter(postmanga__in=mangas).distinct()  
    logger.warning(tags)
    for manga in mangas:
        url= manga.getUrlManga()
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text,'html.parser')
        logger.warning(url)
        chapterList = soup.find_all('div',class_='row')
        if len(chapterList) > 0:
            lastChapter = chapterList[1]
            element= lastChapter.find_all("span")
            #chapInfo = {"title":element[0].get_text(),"url":element[0].find("a").get('href'),"date":element[2].get_text()}
            PostManga.objects.filter(title = manga.title).update(lastChapter=element[0].get_text())
            PostManga.objects.filter(title=manga.title).update(dateLastChapter=element[2].get_text())
      #      logger.warning(lastChapter)
    statusList = ["In corso","Completato","Lasciato momentaneamente"]
    logger.warning(favoriteManga)
    return render(request, 'blog/post_list.html', {'Mangalist': mangas,'FavoriteMangalist': favoriteManga,'TagList':tags,'statusList':statusList})



@login_required
def manga_new(request):
    if request.method == "POST":
        ajax = request.POST.get("ajax")
        logger.warning("manga_new")
        form = NewMangaForm(request.POST,request.FILES)
        logger.warning(ajax)
        if ajax is None:
            if form.is_valid():
                logger.warning("manga_new:form is valid")
                manga=form.save()
                user = request.user
                user.mangaUser.add(manga)
                user.save()
                return redirect('post_list')
            else:
                logger.warning("manga_new:form is not valid")
                return redirect('post_list')
        else:
            form = NewMangaForm()
            return render(request, 'blog/new_manga.html', {'form': form})
    else:
        logger.warning("manga_new else")
        form = NewMangaForm()
        return render(request, 'blog/new_manga.html', {'form': form})



@login_required
def manga_edit(request,title):
    mangaSelected = get_object_or_404(PostManga, title=title)
    if request.method == "POST":
        logger.warning("manga_edit")
        logger.warning(mangaSelected)
        form = NewMangaForm(request.POST,request.FILES,instance=mangaSelected)
        if form.is_valid():

            titleEdited = form.cleaned_data.get('title')
            if title == titleEdited:
                form.save()
            else:
                oldManga =PostManga.objects.filter(title = title).update(title=titleEdited)
                logger.warning(oldManga)
                form.save()
            return redirect('post_list')
    else:
        logger.warning("manga_edit")
        form = NewMangaForm(instance= mangaSelected)
        return render(request, 'blog/manga_edit.html', {'form': form,'manga':mangaSelected})


@login_required
def manga_detail(request, title):
    manga = get_object_or_404(PostManga, title=title)
    url= manga.getUrlManga()
    logger.warning(url)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,'html.parser')
    chapterList = soup.find_all('div',class_='row')[1:]
    #logger.warning(chapterList)
    Chapters = []
    for elem in chapterList:
        element= elem.find_all("span")
        chapInfo = {"title":element[0].get_text(),"url":element[0].find("a").get('href'),"date":element[2].get_text()}
        Chapters.append(chapInfo)
    Tag = {}
    if manga is not None:
        Tag = manga.tags
    return render(request, 'blog/post_detail.html', {'manga': manga,'tags':Tag,'chapters':Chapters})

@login_required
def addManga(request):
    allManga = PostManga.objects.all()
    user = request.user
    myManga = user.mangaUser.all()
    if request.method == "POST":
        form = NewMangaForm(request.POST,request.FILES)
        if form.is_valid():
            manga_new(request)
        else:
            return render(request, 'blog/addManga.html', {"Mangalist":allManga,"myManga":myManga})
    return render(request, 'blog/addManga.html', {"Mangalist":allManga,"myManga":myManga})

@login_required
def user_list(request):
    logger.warning("user_list")  
    allUser = CustomUser.objects.all()
    logger.warning(allUser)
    return render(request, 'blog/all_users.html', {"UserList":allUser})



