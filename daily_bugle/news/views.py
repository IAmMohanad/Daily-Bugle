from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, QueryDict

from django.template import loader

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
# from django.contrib.auth.forms import UserCreationForm

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import Article, Category, User, Comment, Like
from .forms import SignUpForm

import os
from datetime import datetime

#
# User Views
#

@csrf_exempt
@login_required
def index(request):
    #return HttpResponse("Hello, world. You're at the news index.")
    return render(request, 'news/index.html', {})

@csrf_exempt
def signup(request):
    if(request.method == "POST"):
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
        return render(request, 'news/registration/signup.html', {'form':form})

    if(request.method == "GET"):
        form = SignUpForm()

    return render(request, 'news/registration/signup.html', {'form':SignUpForm})

@csrf_exempt
def login(request):
    if(request.method == "GET"):
        return render(request, 'news/registration/login.html', {})
    if(request.method == "POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)
        if(user is None):
            return render(request, 'news/registration/login.html', {'no_user':"Email does not exist"})
        else:
            return render(request, 'news/index.html', {})

#
# Article Views
#

# views.request
# Returns back one article object
def article(request, article_id):
    if request.method == 'GET': # Only accept GET request
        found_article = get_object_or_404(Article, pk=article_id)

        # -- Article Model Format --
        # title = models.CharField(max_length=255)
        # text = models.TextField()
        # pub_date = models.DateTimeField('date published')
        # author_id = models.ForeignKey(User, on_delete=models.CASCADE) # User ID - Many -> One / Many Articles -> One author
        # category_id = models.ForeignKey(Category, on_delete=models.CASCADE) # Category ID - One -> One / One Articles -> One Category

        context = dict()

        context["article"] = {
            "title": found_article.title,
            "text": found_article.text,
            "pub_date": found_article.pub_date,
            "author_name": found_article.author.full_name,
            "category_name": found_article.category.name
        }

        return render(request, 'news/article.html', context)
    else:
        print("views.request: Invalid request type made! Not a GET request.")
        return HttpResponseBadRequest

# views.request
# Returns back one article object
def article_add_new(request):
    if request.method == 'POST': # Only accept POST request
        # -- Article Model Format --
        # title = models.CharField(max_length=255)
        # text = models.TextField()
        # pub_date = models.DateTimeField('date published')
        # author_id = models.ForeignKey(User, on_delete=models.CASCADE) # User ID - Many -> One / Many Articles -> One author
        # category_id = models.ForeignKey(Category, on_delete=models.CASCADE) # Category ID - One -> One / One Articles -> One Category

        new_article = request.POST
        context = dict()

        title = request.POST["new_title"]
        text = request.POST["new_text"]
        pub_date = datetime.now()
        # author = request.session["logged_in_user"]
        request.POST["category_id"]


        try:
            new_article = Article(title=title, text=text, pub_date=pub_date, author=test_user, category=test_category)
            new_article.save()
        except:
            return JsonResponse({"isNewArticleAdded" : False})

        return JsonResponse({"isNewArticleAdded" : True})
    else:
        print("views.request: Invalid request type made! Not a GET request.")
        return HttpResponseBadRequest

# views.article_category
# Returns back all articles within the given category
def article_category(request, category_name):
    if request.method == 'GET': # Only accept GET request
        category_name_id = get_object_or_404(Category, name=category_name).pk
        articles = get_list_or_404(Article, category_id=category_name_id)

        # -- Article Model Format --
        # title = models.CharField(max_length=255)
        # text = models.TextField()
        # pub_date = models.DateTimeField('date published')
        # author_id = models.ForeignKey(User, on_delete=models.CASCADE) # User ID - Many -> One / Many Articles -> One author
        # category_id = models.ForeignKey(Category, on_delete=models.CASCADE) # Category ID - One -> One / One Articles -> One Category

        context = dict()

        for article in articles:
            context[article.pk] = {
                "pk": article.pk,
                "title": article.title,
                "text": article.text,
                "pub_date": article.pub_date,
                "author_name": article.author.full_name,
                "category_name": article.category.name
            }
        return JsonResponse(context)
    else:
        print("views.request: Not invalid request made! Not a GET request.")
        return HttpResponseBadRequest

#
# Comments and Likes
#

@csrf_exempt
def comment(request, article_id):
    if request.method == 'GET':
      question = Comment.objects.filter(article_id_id=article_id)
      print("inside GET")

      AllComments = serializers.serialize("json", question)
      return HttpResponse(AllComments, content_type='application/json')
    if request.method=='POST':
        print("inside post")
        text = request.POST['text']
        NewComment = Comment(text=text,article_id_id=article_id,author_id_id=1)
        NewComment.save()
        idOfComment = NewComment.id
        data={
            'text':text,
            'id':idOfComment
        }
        return JsonResponse(data)

@csrf_exempt
def del_comment(request, article_id,comment_id):
        if request.method=='DELETE':
            Comment.objects.get(pk=comment_id).delete()
            data={
                'id':comment_id
            }
            return JsonResponse(data)

def AllLikes(request, article_id):
    if request.method == 'GET':
        likes = Like.objects.filter(article_id_id=article_id, isLike=1)
        Likescount = likes.count()
        dislikes = Like.objects.filter(article_id_id=article_id, isLike=0)
        dislikescount = dislikes.count()
        print()
        data={
            'totalLikes':Likescount,
            'totalDisLikes':dislikescount
        }
        return JsonResponse(data)


@csrf_exempt
def addorDislike(request, article_id, isLike):
    author_id =request.POST['author_id']
    if request.method == 'POST':
        try:
            check =Like.objects.get(article_id_id=article_id, author_id_id=author_id)
            updateLike = Like.objects.filter(article_id_id=1,author_id_id=author_id).update(isLike=isLike)
            print("addorDislike: GOOD")
        except Like.DoesNotExist:
            print("addorDislike: Is Caught")
            NewLike = Like(isLike= isLike, pub_date='2017-1-23',article_id_id=1,author_id_id=author_id)
            NewLike.save()

    likes = Like.objects.filter(article_id_id=article_id, isLike=1)
    Likescount = likes.count()
    dislikes = Like.objects.filter(article_id_id=article_id, isLike=0)
    dislikescount = dislikes.count()
    print()
    data={
        'totalLikes':Likescount,
        'totalDisLikes':dislikescount
    }
    return JsonResponse(data)
