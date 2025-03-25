import logging
import random
# .forms.editPostForm import EditPostForm
import re
import bs4
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
import requests
from .forms.newMangaForm import NewMangaForm
from .models import PostManga
from .models import Tag
import ast
logger = logging.getLogger("Logger")


# Create your views here.
def post_list(request):
    logger.warning("post_list")
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    mangas = PostManga.objects.all()
    tags = Tag.objects.all()
    for manga in mangas:


        url= manga.getUrlManga()
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text,'html.parser')
        logger.warning(soup)
        chapterList = soup.find_all('div',class_='row')
        if len(chapterList) > 0:
            lastChapter = chapterList[1]
            element= lastChapter.find_all("span")
            #chapInfo = {"title":element[0].get_text(),"url":element[0].find("a").get('href'),"date":element[2].get_text()}
            PostManga.objects.filter(title = manga.title).update(lastChapter=element[0].get_text())
            PostManga.objects.filter(title=manga.title).update(dateLastChapter=element[2].get_text())
            logger.warning(lastChapter)
    return render(request, 'blog/post_list.html', {'Mangalist': mangas,'TagList':tags})

def tableMangaFilter(request):
    logger.warning("filterTag")
    filterTags = request.POST.get("filterTag")
    filterTags = ast.literal_eval(filterTags)
    logger.warning(filterTags)
    resultManga = PostManga.objects.all()
    for elem in filterTags:
        logger.warning(elem)
        resultManga = resultManga.filter(tags=elem)
    json = {}


    return render(request, 'blog/tableManga.html', {'Mangalist': resultManga})

# Create your views here.
def newTag(request):
    logger.warning("newTag")
    newTag = request.POST.get("newTag")
    logger.warning(newTag)
    tag = Tag.objects.filter(tag=newTag).count()
    json = {}
    if(tag != 0):
        logger.warning("Tag esistente")
        json["message"]= "Tag già esistente"
    else:
        items = ["primary","secondary","success","danger","warning","info","light","dark"]
        color = random.choice(items)
        logger.warning("Tag nuovo")
        json["message"] = "Tag nuovo"
        Tag.objects.create(tag=newTag,color=color)
    logger.warning(json)
    return  JsonResponse(json)


#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    mangas = PostManga.objects.all()
    logger.warning(mangas)
    return render(request, 'blog/post_list.html', {'Mangalist': mangas})

def manga_new(request):
    if request.method == "POST":
        form = NewMangaForm(request.POST,request.FILES)
        if form.is_valid():
            logger.warning("manga_new:form is valid")
            manga=form.save()
            return redirect('post_list')
        else:
            logger.warning("manga_new:form is not valid")
            return redirect('post_list')
    else:
        logger.warning("manga_new")
        form = NewMangaForm()
        return render(request, 'blog/new_manga.html', {'form': form})

def manga_edit(request,title):
    mangaSelected = get_object_or_404(PostManga, pk=title)
    if request.method == "POST":
        logger.warning("manga_edit")
        logger.warning(mangaSelected)
    #    mangaSelected = PostManga.objects.get(title=title)
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
        logger.warning("manga_new")
    #    mangaSelected = PostManga.objects.get(title=title)
        form = NewMangaForm(instance= mangaSelected)
        return render(request, 'blog/new_manga.html', {'form': form,'manga':mangaSelected})

#def post_detail(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    return render(request, 'blog/post_detail.html', {'post': post})

def manga_detail(request, title):
    manga = get_object_or_404(PostManga, title=title)

    url= manga.getUrlManga()
    logger.warning(url)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,'html.parser')
    logger.warning(soup)
    chapterList = soup.find_all('div',class_='row')[1:]

    logger.warning(chapterList)
    Chapters = []
    for elem in chapterList:
        element= elem.find_all("span")
    #    logger.warning(element)
        chapInfo = {"title":element[0].get_text(),"url":element[0].find("a").get('href'),"date":element[2].get_text()}
        Chapters.append(chapInfo)
    #logger.warning(urlChapters)

    #"title": manga.css("div.row span a::text").get(),
    #"url": manga.css("div.row span a::text").get(),
    #"lastDate": manga.css("div.row span:nth-child(3)::text").get()

    Tag = {}
    #process = CrawlerProcess(settings={
    #    "FEEDS": {
    #        "items.json": {"format": "json"},
    #    },
    #})
    #process.crawl(HackerNewsSpider)
    
    #process.start()
    #run_spider(HackerNewsSpider)

    data= {}
    #scrapyd = ScrapydAPI('http://localhost:6800')
    #scrapyd.schedule('mangaScrapy', 'name')

    if manga is not None:
        Tag = manga.tags
    return render(request, 'blog/post_detail.html', {'manga': manga,'tags':Tag,'chapters':Chapters})




#def post_edit(request, pk=None):
#    logger.warning("post_edit")
#    logger.warning("post_edit")
#    if(pk != None):
#        post = get_object_or_404(Post,pk=pk)
#    if request.method == "POST":
#        form = EditPostForm(request.POST) #, instance=post
#        logger.warning(form)
#        if form.is_valid():
#            logger.warning("is valid")
        #    logger.warning(post)
#            postForm = form.save(commit=False)
#            #logger.warning(request.POST.get('title'))
#            title= postForm.title
#            text= request.POST.get('text')
#            objPost = Post.objects.get(title=""+title)
#            objPost.author = request.user
#            objPost.published_date = timezone.now()
#            objPost.title = title
#            objPost.text = text
#            objPost.save()
#        return redirect('post_list')
#    else:
#        if(pk != None):
#            form = EditPostForm(instance=post)
#       else:
#            form = EditPostForm()
#        return render(request, 'blog/post_edit.html', {'form': form,'action':'Edit Post'})
