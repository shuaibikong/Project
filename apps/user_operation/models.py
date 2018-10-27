from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField
from users.models import UserProfile
from article.models import Article

User= get_user_model()


# class Comments(models.Model):
#     """
#     用户评论
#     """
#     parent_comment = models.ForeignKey("self", null=True, blank=True, related_name="sub_cat", verbose_name="被评论人(楼层)")
#     article = models.ForeignKey(Article, verbose_name="被评论文章")
#     critics = models.ForeignKey(UserProfile, verbose_name="评论人", related_name="critics_user")
#     by_critics = models.ForeignKey(UserProfile, verbose_name="被评论人", related_name="by_critics_user")
#     content = UEditorField(verbose_name="文章内容", imagePath="article/images/", width=1000, height=300, filePath="article/files/", default="")
#     create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
#
#     class Meta:
#         verbose_name = "用户评论"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.critics
#
#
# class UserOperation(models.Model):
#     OPERATION_TYPE = (
#         (0, '转发'),
#         (1, '收藏'),
#         (2, '感谢'),
#         (3, '评论')
#     )
#     operator = models.ForeignKey(UserProfile, verbose_name="操作用户", related_name="operator_user")
#     auth = models.ForeignKey(UserProfile, verbose_name="被操作用户", related_name="auth_user")
#     operation_type = models.IntegerField(choices=OPERATION_TYPE, verbose_name="操作类型")
#     article = models.ForeignKey(Article, verbose_name="被操作的文章")
#     comments = models.ForeignKey(Comments, verbose_name="文章评论")
#     create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
#
#     class Meta:
#         verbose_name = "用户操作"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.operation_type



class Comments(models.Model):
    """
    用户评论
    """
    parent_comment = models.ForeignKey("self", null=True, blank=True, related_name="sub_cat", verbose_name="被评论人(楼层)")
    article = models.ForeignKey(Article, verbose_name="被评论文章", related_name='comments')
    critics = models.ForeignKey(UserProfile, verbose_name="评论人", related_name="critics_user")
    content = UEditorField(verbose_name="评论内容", imagePath="article/images/", width=1000, height=300, filePath="article/files/", default="")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.critics


class UserOperation(models.Model):
    OPERATION_TYPE = (
        (0, '转发'),
        (1, '收藏'),
        (2, '感谢'),
        (3, '评论'),
        (4, '回复'),
        (5, '举报')
    )
    operator = models.ForeignKey(UserProfile, verbose_name="操作用户", related_name="operator_user")
    operation_type = models.IntegerField(choices=OPERATION_TYPE, verbose_name="操作类型")
    article = models.ForeignKey(Article, verbose_name="被操作的文章")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户操作"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.operation_type


class UserAction(models.Model):
    """
    用户行为
    """
    ACTION = (
        (1, '收藏'),
        (2, '感谢'),
        (3, '举报'))

    action = models.IntegerField(choices=ACTION, default=1)
    user = models.ForeignKey(User, verbose_name="用户")
    article = models.ForeignKey(Article, verbose_name="文章", help_text='文章')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "用户行为"
        verbose_name_plural = verbose_name
        unique_together = ("user", "article", "action")

    def __str__(self):
        return self.username


class UserMessage(models.Model):
    user = models.ForeignKey(User, verbose_name="接收用户", related_name='message')
    title = models.CharField(max_length=30, verbose_name="消息标题", default="")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


# class UserThanks(models.Model):
#     user = models.ForeignKey(User, verbose_name="感谢用户")
#     article = models.ForeignKey(Article, verbose_name="被感谢文章")
#
#     class Meta:
#         verbose_name = "用户感谢"
#         verbose_name_plural = verbose_name
#         unique_together = ("user", "article")
#
#
# class TipOffs(models.Model):
#     user = models.ForeignKey(User, verbose_name="举报用户")
#     article = models.ForeignKey(Article, verbose_name="被举报文章")
#
#     class Meta:
#         verbose_name = "用户举报"
#         verbose_name_plural = verbose_name
#         unique_together = ("user", "article")
