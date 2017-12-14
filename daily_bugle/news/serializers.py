from .models import Article, User,Category,Comment,Article
from rest_framework import serializers

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    comments =  serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='comment-detail',
    )
    class Meta:
        model = Article
        fields = ('url','author','title', 'text','category','pub_date','comments')

class UserSerializer(serializers.ModelSerializer):
    articles =  serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )
    class Meta:
        model = User
        fields = ('email','first_name','last_name','phone_number','articles')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('text','author','pub_date','article')


class CategorySerializer(serializers.ModelSerializer):
    articles =  serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )
    class Meta:
        model = Category
        fields = ('name','articles')
