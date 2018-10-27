from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters, permissions
from rest_framework.pagination import PageNumberPagination

from article.serializers import ArticleSerializers, ArticleDetailSerializers
from article.filters import ArticleFilter
from utils.permissions import IsOwnerOrReadOnly
from .models import Article


class ArticlePagination(PageNumberPagination):
    """
    分页配置
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class ArticleViewset(viewsets.ModelViewSet):
        """
        list:
            所有文章列表
        retrieve:
            获取分类详情
        update:
            编辑文章
        """

        # queryset = Article.objects.all()
        serializer_class = ArticleSerializers
        pagination_class = ArticlePagination
        filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
        filter_class = ArticleFilter
        search_fields = ('author', 'title', 'article_type')
        ordering_fields = ('click_num', 'thanks_num', 'fav_num', 'forwarding_num', 'comments_num')

        def get_queryset(self):
            article = Article.objects.all()
            return article

        def get_serializer_class(self):
            if self.action == 'retrieve':
                return ArticleDetailSerializers
            elif self.action == "update" or self.action == "create" or self.action == "partial_update":
                return ArticleSerializers

            return ArticleDetailSerializers

        def get_permissions(self):
            # 根据当前的method 来返回相应的权限

            # 只有viewset才有action 并从中取到各种数据 状态与mixin方法一致
            if self.action == 'create':
                return [permissions.IsAuthenticated()]
            elif self.action == "update" or self.action == "destroy" or self.action == "partial_update":
                return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
            else:
                return []

        def perform_update(self, serializer):
            instance = serializer.save()
            instance.update_time = datetime.now()
            instance.save()

