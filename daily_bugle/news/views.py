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


import os
from datetime import datetime

#
# User Views
#

@csrf_exempt
#@login_required
def index(request):
    #articlesList = getArticles()
    context = {}
    context["articlesList"] = getArticles()
    context["currentPage"] = "index"

    #if request.user.is_authenticated():
        #context["user"] = request.user

    return render(request, 'news/index.html', context)
    """# redirect to the value of next if it is entered,
    otherwise to /accounts/profile/return
    redirect(request.POST.get('next','/accounts/profile/'))"""

@csrf_exempt
def signup(request):
    if(request.method == "POST"):
        #if form is valid, authenticate use and log them in.
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
            user = authenticate(email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
            loginUser(request, user)
            current_user = user
            return render(request, 'news/index.html', {'user':user.id})
        else:#not valid, return with errors
            return render(request, 'news/registration/signup.html', {'form':form})

    #return empty sign up form
    if(request.method == "GET"):
        form = SignUpForm()

    return render(request, 'news/registration/signup.html', {'form':form})

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
            loginUser(request, user)
            current_user = user.id
            return redirect('/')
            #return render(request, 'news/index.html', {'user':current_user})
            #next_url = request.GET.get('next')
            #if next_url:
            #    return HttpResponseRedirect(next_url)
            #else:
            #    return render(request, 'news/index.html', {'user':current_user})


@csrf_exempt
def logout(request):
    logoutUser(request)
    return redirect('/')


@csrf_exempt
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
            return render(request, 'news/updateProfile.html', {'form': form, 'saved': 'success', 'user': request.user.id})
        else:
            # will go to the the ajax error: data.responseText
            return render(request, 'news/updateProfile.html', {'form': form, 'saved': 'failed'})


#
# Article Views
#

def getArticles():
    total_articles = Article.objects.all().count()
    articles = Article.objects.order_by("-pk")[:5] #.objects.all()

    articlesList = []

    for article in articles:
        articlesList.append({
            "id": article.pk,
            "title": article.title,
            "text": article.text,
            "pub_date": article.pub_date
            #"author_name": article.author.first_name,
            #"category_name": article.category.name
        })
    return articlesList

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
