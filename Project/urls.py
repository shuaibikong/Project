"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token


import xadmin

from Project.settings import MEDIA_ROOT
from article.views import ArticleViewset
from user_operation.views import CommentsViewset, UserOperationAPIView, UserfavViewset, UsermessageViewset
from users.views import SmsCodeViewset, UserViewset

router = DefaultRouter()

#文章url
router.register(r'articles', ArticleViewset , base_name="articles")

#注册校验url
router.register(r'codes', SmsCodeViewset, base_name='codes')

#用户注册url
router.register(r'users', UserViewset, base_name='users')

#用户操作url
router.register(r'operation', UserOperationAPIView, base_name='operation')

#用户评论url
router.register(r'comments', CommentsViewset, base_name='comments')

#用户收藏url
router.register(r'userfav', UserfavViewset, base_name='userfav')

#用户消息url
router.register(r'usermessage', UsermessageViewset, base_name='usermessage')


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    url(r'^', include(router.urls)),

    url(r'docs/', include_docs_urls(title="lanya")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 配置获取 JWT 的url  jwt的认证接口
    url(r'^login/$', obtain_jwt_token),
    #
    # #配置获取token的 url  drf自带的验证模式
    # url(r'^api-token-auth/', views.obtain_auth_token),

    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    #第三方登录url
    url('', include('social_django.urls', namespace='social'))
]
