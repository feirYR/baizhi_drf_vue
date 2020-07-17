import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user.models import UserInfo
from user.utils import check_user
from django_redis import get_redis_connection

class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024,read_only=True,help_text='用户token')
    code = serializers.CharField(max_length=6, write_only=True,required=True,help_text='手机验证码')

    class Meta:
        model = UserInfo
        fields = ('id','username', 'password', 'phone','token','code')

        extra_kwargs = {
            'id':{
                'read_only': True
            },
            'username': {
                'read_only': True
            },
            'password': {
                # 'min_length': 6,
                'required':True,
                'write_only': True
            },
            'phone': {
                'write_only': True
            },
        }

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        code = attrs.get('code')
        print(39,code)
        print(password, type(password))
        if not re.match(r'^1[3-9][0-9]{9}', phone):
            print('手机格式验证失败')
            raise serializers.ValidationError('手机号格式错误')
        print('手机格式验证成功')
        # user = UserInfo.objects.filter(phone=phone).first()
        try:
            user= check_user(phone)
        except:
            user = None
        if user:
            raise serializers.ValidationError('该手机号已注册')
        print(22222222)
        redis_connect = get_redis_connection('sms')
        sms_code = redis_connect.get('sms_expire_%s' % phone)
        print('验证码',code,sms_code.decode())
        if code != sms_code.decode():
            raise serializers.ValidationError('输入验证码有误')
        return attrs

    def create(self, validated_data):
        print(3333333)
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        print(phone,password)
        hasher_password = make_password(password)
        username = phone
        print(53,'username')
        user = UserInfo.objects.create(username=username, phone=phone, password=hasher_password)
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        return user
