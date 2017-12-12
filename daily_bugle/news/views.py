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
from rest_framework import viewsets
from .serializers import ArticleSerializer,UserSerializer,CommentSerializer,CategorySerializer
#
# User Views
#


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

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
            "pk": found_article.pk,
            "title": found_article.title,
            "text": found_article.text,
            "pub_date": found_article.pub_date,
            "author_name": found_article.author.first_name,
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
            context[article] = {
                "pk": article.pk,
                "title": article.title,
                "text": article.text,
                "pub_date": article.pub_date,
                "author_name": article.author.first_name,
                "category_name": article.category.name
            }
        return JsonResponse(context)
    else:
        print("views.request: Not invalid request made! Not a GET request.")
        return HttpResponseBadRequest

#
# Comments and Likes
#


def findUser(author_id):
    print ("author id is "+ str(author_id))
    user = User.objects.get(id=1)
    print (user)
    first_name= user.first_name
    userInfo ={
            'First_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
    }
    return userInfo
@csrf_exempt
def comment(request, article_id):

    if request.method == 'GET':

        comments = get_list_or_404(Comment, article_id=article_id)
        print ("jfdjfld helloplp")
        context = dict()

        for comment in comments:
            context[comment.pk] = {
                "pk": comment.pk,
                "text": comment.text,
                "pub_date": comment.pub_date.strftime("%d, %b %Y"),
                "author": findUser(comment.author_id)["First_name"],
                "email":findUser(comment.author_id)["email"]
            }

        return JsonResponse(context)

    if request.method=='POST':
        print("inside post")
        RequestData = QueryDict(request.body)#Querydict is used to retrived the new price of the ITEM
        text= RequestData.get('text')
        #text = request.POST.get("name")
        print("Inside Text: " + text)
        NewComment = Comment(text=text,article_id=article_id,author_id=1)
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
        likes = Like.objects.filter(article_id=article_id, isLike=1)
        Likescount = likes.count()
        dislikes = Like.objects.filter(article_id=article_id, isLike=0)
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
            check =Like.objects.get(article_id=article_id, author_id=author_id)
            updateLike = Like.objects.filter(article_id=1,author_id=author_id).update(isLike=isLike)
            print("addorDislike: GOOD")
        except Like.DoesNotExist:
            print("addorDislike: Is Caught")
            NewLike = Like(isLike= isLike, pub_date='2017-1-23',article_id=1,author_id=author_id)
            NewLike.save()

    likes = Like.objects.filter(article_id=article_id, isLike=1)
    Likescount = likes.count()
    dislikes = Like.objects.filter(article_id=article_id, isLike=0)
    dislikescount = dislikes.count()
    print()
    data={
        'totalLikes':Likescount,
        'totalDisLikes':dislikescount
    }
    return JsonResponse(data)
