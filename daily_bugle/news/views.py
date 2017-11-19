from django.shortcuts import render

from .models import Article, Category
from django.http import JsonResponse

#
# Article Views
#

# views.request
# Returns back one article object
def article(request, article_id):
    if request.method == 'GET': # Only accept GET request
        found_article_object = article_id # Allow category_name to be found_category_id for submitting error
        try:
            found_article_object = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            # If category_name is not found
            print("views.request: Invalid article searched! Article" + found_article_object + " does not exist.")
            return HttpResponseBadRequest

        # -- Article Model Format --
        # title = models.CharField(max_length=255)
        # text = models.TextField()
        # pub_date = models.DateTimeField('date published')
        # author_id = models.ForeignKey(User, on_delete=models.CASCADE) # User ID - Many -> One / Many Articles -> One author
        # category_id = models.ForeignKey(Category, on_delete=models.CASCADE) # Category ID - One -> One / One Articles -> One Category

        article = {
            "pk": article.pk,
            "title": article.title,
            "text": article.text,
            "pub_date": article.pub_date,
            "author_name": "Jack", # article.author_id,
            "category_name": "Racing" # article.category_id
        }

        return render(request, 'polls/article.html', article)
    else:
        print("views.request: Invalid request type made! Not a GET request.")
        return HttpResponseBadRequest

# views.article_category
# Returns back all articles within the given category
def article_category(request, category_name):
    if request.method == 'GET': # Only accept GET request
        found_category_id = category_name # Allow category_name to be found_category_id for submitting error
        try:
            found_category_id = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            # If category_name is not found
            print("views.request: Invalid category searched! " + found_category_id + " category does not exist.")
            return HttpResponseBadRequest

        searchedArticlesList = Article.objects.filter(category_id=found_category_id)
        jsonResponse_articleList = dict()

        # If no Articles found within the category
        if not searchedArticlesList:
            jsonResponse_searchedArticlesList = { "articles_found_count": 0 }
            return JsonResponse(jsonResponse_searchedArticlesList)

        # -- Article Model Format --
        # title = models.CharField(max_length=255)
        # text = models.TextField()
        # pub_date = models.DateTimeField('date published')
        # author_id = models.ForeignKey(User, on_delete=models.CASCADE) # User ID - Many -> One / Many Articles -> One author
        # category_id = models.ForeignKey(Category, on_delete=models.CASCADE) # Category ID - One -> One / One Articles -> One Category

        for article in searchedArticle:
            jsonResponse_articleList.update(dict({
            "pk": article.pk,
            "title": article.name,
            "text": article.text,
            "pub_date": article.description,
            "author_id": article.price,
            "category_id": article.price
            }))
        return JsonResponse(jsonResponse_searchedArticle)
    else:
        print("views.request: Not invalid request made! Not a GET request.")
        return HttpResponseBadRequest
