from django.db import models

# Create your models here.
class User(model.Models):
	full_name = models.CharField(length=255)
	email = models.EmailField(length=254, unique=True)
	password = models.CharField(length=255)
	phone_number = models.CharField(length=20)
    def __str__(self):
        return self.question_text

class Article(model.Models):
	title = models.CharField(length=255)
	text = models.TextField()
	pub_date = models.DateTimeField('date published')
	author_id = # User ID - Many -> One / Many Articles -> one author
	comment_id = # many -> many many / many comments posted to many articles
    def __str__(self):
        return self.question_text

class Category(model.Models):
	name =
    def __str__(self):
        return self.question_text

class Comment(model.Models):
    text = models.TextField()
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text
