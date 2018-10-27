from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import mixins, viewsets, filters, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from article.models import Article
from user_operation.models import UserOperation, Comments, UserMessage, UserAction
from user_operation.serializers import UserOperationSerializer, CommentsSerializer, UserActionDetailSerializer,\
    UserMessageSerializer
from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()


class UserOperationAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserOperationSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserOperation.objects.filter(operator=self.request.user)

    def create(self, request, *args, **kwargs):
        article = Article.objects.get(id=request.data['article'])
        dict = {
            'operator':request.user,
            'operation_type': request.data['operation_type'],
            'article': article.id
        }
        serializer = self.get_serializer(data=dict)
        serializer.is_valid(raise_exception=True)
        operation = self.perform_create(serializer)
        article = operation.article
        user = operation.operator

        if operation.operation_type == 0:
            article.forwarding_num += 1
            article.save()
            # 转发

        if operation.operation_type == 1:
            article.fav_num += 1
            article.save()
            # 添加收藏

            is_fav = UserAction.objects.filter(user=user, article=article, action=1)
            if is_fav:
                response = {"detail": "请不要重复收藏"}
                operation.delete()
                return Response(response, status=status.HTTP_403_FORBIDDEN, headers={})

            else:
                userfav = UserAction()
                userfav.action = 1
                userfav.user = user
                userfav.article = article
                userfav.save()

        #添加感谢
        if operation.operation_type == 2:
            article.thanks_num += 1
            article.save()

            is_thanks = UserAction.objects.filter(user=user, article=article, action=2)
            if is_thanks:
                response = {"detail": "请不要重复感谢"}
                operation.delete()
                return Response(response, status=status.HTTP_403_FORBIDDEN, headers={})

            else:
                userthanks = UserAction()
                userthanks.action = 2
                userthanks.user = user
                userthanks.article = article
                userthanks.save()



        if operation.operation_type == 3:
            comment = Comments()
            comment.article = article
            comment.critics = request.user
            comment.content = request.data.get('content')
            comment.save()

            #发送站内信息
            message = UserMessage()
            message.user = article.author
            message.title = "{user1} 回复了 {user2}".format(user1=request.user.nick_name
                                                                if request.user.nick_name else request.user.username,
                                                                user2=article.title)
            message.message = request.data.get('content')
            message.save()

        elif operation.operation_type == 4:
            comment = Comments()
            by_critics = Comments.objects.get(id=request.data['by_critics'])
            comment.parent_comment = by_critics
            comment.article = article
            comment.critics = request.user
            comment.content = request.data.get('content')
            comment.save()

            message = UserMessage()
            message.user = by_critics.critics
            message.title = "{user1} 回复了 {user2}".format(user1=request.user.nick_name
                                                                if request.user.nick_name else request.user.username,
                                                                user2=article.title)
            message.message = request.data.get('content')
            message.save()

        elif operation.operation_type == 5:
            #添加举报
            is_tipoff = UserAction.objects.filter(user=user, article=article, action=2)
            if is_tipoff:
                response = {"detail": "请不要重复举报"}
                operation.delete()
                return Response(response, status=status.HTTP_403_FORBIDDEN, headers={})

            else:
                usertipoff = UserAction()
                usertipoff.action = 3
                usertipoff.user = user
                usertipoff.article = article
                usertipoff.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class CommentsViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.all()


class UserfavViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        用户收藏
    retrieve:
        判断某篇文章是否已经收藏
    destroy:
        取消收藏
    """

    serializer_class = UserActionDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    #通过文章的id获取详情判断是否收藏
    lookup_field = "article_id"

    def get_queryset(self):
        # 返回当前用户的收藏信息
        return UserAction.objects.filter(user=self.request.user, action=1)


class UserthanksViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        判断某篇文章是否已经感谢
    """

    serializer_class = UserActionDetailSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    #通过文章的id获取详情判断是否
    lookup_field = "article_id"

    def get_queryset(self):
        # 返回当前用户的收藏信息
        return UserAction.objects.filter(user=self.request.user, action=1)


class UsermessageViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
     list:
         用户消息
     retrieve:
         消息详情 点击后变为已读
     destroy:
         删除消息
     """
    serializer_class = UserMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        # 返回当前用户的收藏信息
        return UserMessage.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        instance.has_read = True
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
