from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,JsonResponse,QueryDict
from .models import Comment
from .models import Like
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    return render(request, 'news/AllComments.html', {})

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
        NewComment = Comment(text=text, pub_date='2017-1-23',article_id_id=article_id,author_id_id=1)
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

def likes(request, article_id):
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
