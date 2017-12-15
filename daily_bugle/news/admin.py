from django.contrib import admin

from .models import Article,User,Category,Comment,Like

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)
