import xadmin

from .models import Article


class ArticleAdmin:
    style_fields = {"content": "ueditor"}


xadmin.site.register(Article, ArticleAdmin)
