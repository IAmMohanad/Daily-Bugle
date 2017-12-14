from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    #USERNAME_FIELD
    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    #email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255) # We need to store Hashed Password - Figure out later
    phone_number = models.IntegerField(blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE) # User ID - Many -> One / Many Articles -> One author
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.CASCADE) # Category ID - One -> One / One Articles -> One Category

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User) # User ID - Many -> One / Many Articles -> one author
    pub_date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article,related_name='comments',on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Like(models.Model):
    isLike = models.NullBooleanField()
    author = models.ForeignKey(User) # User ID - Many -> One / Many Articles -> one author
    pub_date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)
