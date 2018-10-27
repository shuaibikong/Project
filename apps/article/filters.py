import django_filters
from django.db.models import Q

from .models import Article


class ArticleFilter(django_filters.rest_framework.FilterSet):
    """
    文章的过滤类
    """
    category = django_filters.NumberFilter(method='category_filter', help_text="文章分类")

    def category_filter(self, queryset, name, value):
        return queryset.filter(article_type=value)


    class Meta:
        model = Article
        fields = ['category']