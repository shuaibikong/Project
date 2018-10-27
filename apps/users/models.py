from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    nick_name = models.CharField(max_length=30, verbose_name="昵称", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="female", verbose_name="性别")
    user_type = models.IntegerField(choices=((0, "牙医"), (1, "普通用户")), default=1, verbose_name="用户类别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name="地址")
    face_image = models.ImageField(upload_to="image/user_face/%Y/%m", null=True, blank=True, max_length=100)
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        name = self.nick_name if self.nick_name else self.username
        return name


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.IntegerField(choices=((0, "注册"), (1, "找回密码"), (2, "修改邮箱")), verbose_name="验证码类型")
    send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}(1)'.format(self.code, self.email)


# class MobileVerifyCode(models.Model):
#     """
#     短信验证码
#     """
#     code = models.CharField(max_length=10, verbose_name='验证码')
#     mobile = models.CharField(max_length=11, verbose_name='手机号')
#     send_type = models.IntegerField(choices=((0, "注册"), (1, "找回密码"), (2, "修改手机号")), verbose_name="验证码类型")
#     send_time = models.DateTimeField(verbose_name="发送时间", default=datetime.now)
#
#     class Meta:
#         verbose_name = '短信验证码'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return '{0}(1)'.format(self.code, self.mobile)