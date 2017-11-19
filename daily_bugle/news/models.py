from django.db import models

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255) # We need to store Hashed Password - Figure out later
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk)

class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE) # User ID - Many -> One / Many Articles -> One author
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # Category ID - One -> One / One Articles -> One Category

    def __str__(self):
        return str(self.pk)

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User) # User ID - Many -> One / Many Articles -> one author
    pub_date = models.DateTimeField('date published')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

class Like(models.Model):
    isLike = models.NullBooleanField()
    author = models.ForeignKey(User) # User ID - Many -> One / Many Articles -> one author
    pub_date = models.DateTimeField('date published')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
