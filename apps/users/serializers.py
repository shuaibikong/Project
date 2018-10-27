import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from Project.settings import REGEX_MOBILE, REGEX_EMAIL
from users.models import EmailVerifyRecord

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    """
    验证码发送校验
    """
    uname = serializers.CharField()

    def validate_email(self, uname):
        """
        验证账号
        """
        # 验证账号是否合法
        if not re.match(REGEX_MOBILE, uname):
            if not re.match(REGEX_EMAIL, uname):
                raise serializers.ValidationError("账号格式错误")

        #是否注册
        if User.objects.filter(Q(mobile=uname)|Q(email=uname)):
            raise serializers.ValidationError("用户已经存在")

        #验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if EmailVerifyRecord.objects.filter(send_time__gt=one_mintes_ago, mobile=uname):
            raise serializers.ValidationError("距离上次发送未超过60s")

        return uname


class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册校验
    """
    code = serializers.CharField(required=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={"required": "请输入验证码",
                                                 "blank": "请输入验证码",
                                                 "max_length": "验证码格式错误",
                                                 "min_length": "验证码格式错误"},
                                 help_text='验证码', write_only=True)
    username = serializers.CharField(help_text="用户名", label='用户名', required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='账号已存在')])
    password = serializers.CharField(help_text="密码",
        style={'input_type': 'password'}, label='密码', write_only=True
    )

    def create(self, validated_data):
        #拿到创建后的用户
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


    def validate_code(self, code):
        verify_records = EmailVerifyRecord.objects.filter(email=self.initial_data.get("username"), send_type=0).order_by(
            '-send_time'
        )
        if verify_records:
            #只取最后一条验证码记录进行校验
            last_records = verify_records[0]
            #有效期为五分钟
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if last_records.send_time < five_mintes_ago:
                raise serializers.ValidationError("验证码过期")

            if last_records.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        """
        作用于所有的serializer字段之上 attrs为校验后所有字段的dict
        """

        #前端只传进了username 将mobile与username统一
        if re.match(REGEX_MOBILE, attrs["username"]):
            attrs['mobile'] = attrs["username"]
        elif re.match(REGEX_EMAIL, attrs["username"]):
            attrs['email'] = attrs['username']


        #删除掉校验后的code字段 不保存进user表中
        del attrs["code"]
        return attrs


    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化
    """

    class Meta:
        model = User
        fields = ("nick_name", "gender", "birthday", "email", "mobile", "face_image", "address")