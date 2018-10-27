import random
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render
from django.core.mail import send_mail

from rest_framework import mixins, permissions, authentication
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from Project.settings import REGEX_MOBILE, REGEX_EMAIL, APIKEY, EMAIL_FROM
from users.models import EmailVerifyRecord
from users.serializers import UserDetailSerializer, UserRegSerializer, SmsSerializer
from utils.yunpian import YunPian

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证 来替换django本身的验证 可以通过username或mobile查询出用户
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(email=username)|Q(mobile=username)|Q(username=username))
            if user.check_password(password):#校验密码
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, GenericViewSet):
    """
    发送验证码
    """

    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字验证码
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(random.choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uname = serializer.validated_data['uname']

        if re.match(REGEX_MOBILE, uname):
            #发送短信
            yunp_pian = YunPian(APIKEY)

            code = self.generate_code()

            sms_status = yunp_pian.send_sms(code, uname)
            # 判断是否发送成功
            if sms_status["code"] != 0:
                return Response({
                    'uname': sms_status["msg"]
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                code_record = EmailVerifyRecord(code=code, email=uname, send_type="注册")
                code_record.save()

                return Response({
                    'uname': uname
                }, status=status.HTTP_201_CREATED)

        if re.match(REGEX_EMAIL, uname):
            #发送邮件
            code = self.generate_code()
            email_title = "蓝牙注册验证码"
            email_body = "以下为您的验证码: {}".format(code)
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [uname])
            if send_status:
                pass
                # 判断是否发送成功
                if send_status["code"] == 0:
                    return Response({
                        'uname': send_status["msg"]
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    email_record = EmailVerifyRecord()
                    email_record.code = code
                    email_record.email = uname
                    email_record.send_type = "注册"
                    email_record.save()

                    return Response({
                        'uname': uname
                    }, status=status.HTTP_201_CREATED)




class UserViewset(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer

        return UserDetailSerializer

    def get_permissions(self):
        #根据当前的method 来返回相应的权限
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []

        return []


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #拿到返回的user信息 并返回token放入
        user = self.perform_create(serializer)

        #用jwt生成的token
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.nick_name else user.email

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        #当进入用户详情页时, 返回当前用户
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
