from rest_framework import serializers

from article.models import Article
from article.serializers import ArticleSerializers
from user_operation.models import UserOperation, Comments
from users.serializers import UserDetailSerializer
from .models import UserAction, UserMessage


class UserOperationSerializer(serializers.ModelSerializer):
    operator = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    article = serializers.PrimaryKeyRelatedField(required=True, label='文章', queryset=Article.objects.all())

    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    # def validate_article(self, article):
    #     if article:
    #         return article
    #     else:
    #         raise serializers.ValidationError('文章不存在')

    class Meta:
        model = UserOperation
        fields = "__all__"


class CommentsSerializer2(serializers.ModelSerializer):
    article = ArticleSerializers()
    critics = UserDetailSerializer()
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comments
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    sub_cat = CommentsSerializer2(many=True)
    article = ArticleSerializers()
    critics = UserDetailSerializer()
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comments
        fields = "__all__"


class UserActionDetailSerializer(serializers.ModelSerializer):
    article = ArticleSerializers()
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserAction
        fields = ('article', 'id', "add_time")


class UserMessageSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer
    # add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserMessage
        fields = ("__all__")