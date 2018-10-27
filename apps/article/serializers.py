from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UserDetailSerializer
# from user_operation.serializers import CommentsSerializer
from .models import Article

User = get_user_model()


class ArticleSerializers(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
            model = Article
            fields = ("author", "title", "content", "article_type")


class ArticleDetailSerializers(serializers.ModelSerializer):

    author = UserDetailSerializer()
    # comments = CommentsSerializer(many=True)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = "__all__"


