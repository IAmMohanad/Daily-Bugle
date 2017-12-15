from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, JsonResponse, QueryDict

from django.template import loader

from django.contrib.auth import login as loginUser, logout as logoutUser, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
# from django.contrib.auth.forms import UserCreationForm

from django.core import serializers

from django.views.decorators.csrf import csrf_exempt

from .models import Article, Category, User, Comment, Like
from .forms import SignUpForm, UserUpdateForm

from rest_framework.permissions import IsAuthenticated

import os
from datetime import datetime
from rest_framework import viewsets
from .serializers import ArticleSerializer,UserSerializer,CommentSerializer,CategorySerializer
#
# User Views
#
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

"""
Homepage. Loads the 5 latest articles, either from all categories if no category id is in get request or from the specific category is the id is present.
"""
#@csrf_exempt
#@login_required
def index(request):
    context = {}
    category = request.GET.get('category')#print(str(request.GET.get('category')+"........"))
    context["articlesList"] = getArticles(category)
    context["currentPage"] = "index"

    return render(request, 'news/index.html', context)
    """# redirect to the value of next if it is entered,
    otherwise to /accounts/profile/return
    redirect(request.POST.get('next','/accounts/profile/'))"""

"""
Allows the user to sign up. If GET request, return an empty SignUpForm.
If POST request & form is valid create a new user object, login user then redirect them to index.
If  POST request & form is NOT valid, return to the signup page with the form populated with the input data.
"""
#@csrf_exempt
def signup(request):
    if(request.method == "POST"):
        #if form is valid, authenticate use and log them in.
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
            user = authenticate(email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
            loginUser(request, user)
            current_user = user
            #return render(request, 'news/index.html', {'user':user.id})
            return redirect('/')
        else:#not valid, return with errors
            return render(request, 'news/registration/signup.html', {'form':form})

    #return empty sign up form
    if(request.method == "GET"):
        form = SignUpForm()

    return render(request, 'news/registration/signup.html', {'form':form})

"""
Log in the user.
If GET request return the log in page.
If POST request & user was succesfully authenticated log in user and redirect to homepage.
If POST request & user was NOT succesfully authenticated, return to the log in page with error message.
"""
#@csrf_exempt
def login(request):
    if(request.method == "GET"):
        return render(request, 'news/registration/login.html', {})
    if(request.method == "POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)

        if(user is None):
            return render(request, 'news/registration/login.html', {'no_user':"Email or password are incorrect."})
        else:
            loginUser(request, user)
            current_user = user.id
            return redirect('/')
            #return render(request, 'news/index.html', {'user':current_user})
            #next_url = request.GET.get('next')
            #if next_url:
            #    return HttpResponseRedirect(next_url)
            #else:
            #    return render(request, 'news/index.html', {'user':current_user})


#@csrf_exempt
def logout(request):
    logoutUser(request)
    return redirect('/')

"""
Allows the user to update their data. [name, email, phone]
If GET returns the profile form with relevant data pre-populated.
If POST retrieves the users data based on the users id and updates the relevant database entry.
"""
#@csrf_exempt
@login_required
def updateProfile(request):
    if(request.method == "GET"):
        data = {'id' : request.user.id, 'email' : request.user.email, 'first_name' : request.user.first_name, 'last_name' : request.user.last_name, 'phone_number': request.user.phone_number}
        form = UserUpdateForm(initial=data)
        return render(request, 'news/updateProfile.html', {'form': form, 'user': request.user, "currentPage": "index"})
    if(request.method == "POST"):
        # get the model from the db
        model, created = User.objects.get_or_create(pk = request.user.id)
        # create the form based on the model, but with the request data overriding the model data
        form = UserUpdateForm(request.POST, instance = model)

        # save if valid
        if form.is_valid():
            form.save()
            return render(request, 'news/updateProfile.html', {'form': form, 'saved': 'success', 'user': request.user})
        else:
            return render(request, 'news/updateProfile.html', {'form': form, 'saved': 'failed'})

"""
Returns 5 articles.
If category is NOT set returns the 5 most recent articles sorted in descending order based on their id.
If category is set, returns 5 articles AND if their category_id matches the category in the request.
"""
#@csrf_exempt
def getArticles(category):
    total_articles = Article.objects.all().count()

    if category is not None:
        articles = Article.objects.filter(category_id=category).order_by("-pk")[:5]
    else:
        articles = Article.objects.order_by("-pk")[:5]
    articlesList = []

    for article in articles:
        articlesList.append({
            "id": article.pk,
            "title": article.title,
            "text": article.text,
            "pub_date": article.pub_date,
            "author_name": article.author.first_name,
            "category_name": article.category.name
        })
    return articlesList

"""
articlesAmount repersents the number of articles that are currently on the HTML page.
Returns 5 articles based on the articlesAmount variable.
For example, if articlesAmount is 5, returns articles 6-11.
If category is NOT set returns most recent articles.
If category is set, returns articles based on their category_id.
"""
#@csrf_exempt
def loadMoreArticles(request, articlesAmount):
    total_articles = Article.objects.all().count()
    category = request.GET.get('category')
    if int(articlesAmount) != 0 and articlesAmount is not None:
        if int(articlesAmount)  <= total_articles:
            if(category != "null"):
                articles = Article.objects.filter(category_id=int(category)).order_by("-pk")[int(articlesAmount) : int(articlesAmount)  + 5]
            else:
                print("entered here")
                articles = Article.objects.order_by("-pk")[int(articlesAmount) : int(articlesAmount)  + 5]
                print("go to here")

            articlesList = []

            for article in articles:
                articlesList.append({
                    "id": article.pk,
                    "title": article.title,
                    "text": article.text,
                    "pub_date": article.pub_date,
                    "author_name": article.author.first_name,
                    "category_name": article.category.name
                })
            return JsonResponse({"articlesList": articlesList})

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
            "category_name": found_article.category.name,
            "user": request.user
        }
        context["user"] = request.user

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
    user = User.objects.get(id=author_id)
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
        context = dict()
        for comment in comments:
            context[comment.pk] = {
                "pk": comment.pk,
                "text": comment.text,
                "pub_date": comment.pub_date.strftime('%d, %b %Y'),
                "author": findUser(comment.author_id)["First_name"],
                "email":findUser(comment.author_id)["email"]
            }
        return JsonResponse(context)
    if(request.user.is_authenticated()):
        if request.method=='POST':
            current_user= request.user
            RequestData = QueryDict(request.body)#Querydict is used to retrived the new price of the ITEM
            text= RequestData.get('text')
            #text = request.POST.get("name")
            NewComment = Comment(text=text,article_id=article_id,author_id=current_user.id)
            NewComment.save()
            comments = get_list_or_404(Comment, article_id=article_id)
            context = dict()
            for comment in comments:
                context[comment.pk] = {
                    "pk": comment.pk,
                    "text": comment.text,
                    "pub_date": comment.pub_date.strftime('%d, %b %Y'),
                    "author": findUser(comment.author_id)["First_name"],
                    "email":findUser(comment.author_id)["email"]
                }
            return JsonResponse(context)
        '''idOfComment = NewComment.id
        commentsObj = get_object_or_404(Comment, id=idOfComment)
        context = dict()
        print ("object primary key is ")
        print ("object primary key is "+ NewComment.text)
        data = {
            "pk": NewComment.pk,
            "text": NewComment.text,
            "pub_date": NewComment.pub_date,
            "author": findUser(NewComment.author_id)["First_name"],
            "email":findUser(NewComment.author_id)["email"]
        }

        #data={
        #    'text':text,
        #    'id':idOfComment
        #}
        return JsonResponse(data)'''

@login_required
@csrf_exempt
def del_comment(request, article_id,comment_id):
        if request.method=='DELETE':
            comment = Comment.objects.get(pk=comment_id)
            if(request.user.id == comment.author_id):
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
    current_user= request.user
    if request.method == 'POST':
        try:
            print ("user id is "+str(current_user.id))
            check =Like.objects.get(article_id=article_id, author_id=current_user.id)
            updateLike = Like.objects.filter(article_id=article_id,author_id=current_user.id).update(isLike=isLike)
        except Like.DoesNotExist:
            NewLike = Like(isLike= isLike, pub_date='2017-1-23',article_id=article_id,author_id=current_user.id)
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
