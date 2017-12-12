from .models import Article, User,Category,Comment,Article
from rest_framework import serializers


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=False,queryset=Category.objects.all())
    #author = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    author = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail'
    )
    category = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='category-detail'
    )
    comments =  serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='comment-detail'
    )
    class Meta:
        model = Article
        fields = ('author','title', 'text','category','pub_date','comments')
    def to_representation(self, obj):
        data = super().to_representation(obj)
        request = self.context["request"]
        return data

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
    author = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail'
    )
    """articles =  serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )"""
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


"""
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk)
"""
