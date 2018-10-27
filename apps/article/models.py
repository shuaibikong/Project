from datetime import datetime

from django.db import models

from users.models import UserProfile
from DjangoUeditor.models import UEditorField
# Create your models here.


class Article(models.Model):
    CATEGORY_TYPE = (
        (1, "讨论"),
        (2, "询问"),
        (3, "记录"),
        (4, "牙套"),
        (5, "智齿"),
        (6, "种植"),
    )
    author = models.ForeignKey(UserProfile, verbose_name="发表用户")
    title = models.CharField(max_length=100, verbose_name="话题标题")
    content = UEditorField(verbose_name="文章内容", imagePath="article/images/", width=1000, height=300, filePath="article/files/", default="")
    article_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="文章类别", help_text="文章类别")
    click_num = models.IntegerField(verbose_name="被点击次数", default=0)
    thanks_num = models.IntegerField(verbose_name="被感谢次数", default=0)
    fav_num = models.IntegerField(verbose_name="被收藏次数", default=0)
    forwarding_num = models.IntegerField(verbose_name="被转发次数", default=0)
    comments_num = models.IntegerField(verbose_name="被评论次数", default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", default=datetime.now)
    update_time = models.DateTimeField(null=True, blank=True, verbose_name="文章更新时间")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
