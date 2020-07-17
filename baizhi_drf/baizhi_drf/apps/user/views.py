import random
import re

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from baizhi_drf.libs.geetest import GeetestLib
from user.models import UserInfo
from user.utils import check_user
from utils.Response import MyResponse
from rest_framework.generics import CreateAPIView,DestroyAPIView
from user.serializers import UserModelSerializer
from utils.send_msg import SMSSend
from django_redis import get_redis_connection
pc_geetest_id = "6f91b3d2afe94ed29da03c14988fb4ef"
pc_geetest_key = "7a01b1933685931ef5eaf5dabefd3df2"


class Captche(APIView):
    user_id = 0

    # status = False
    def get(self, request):
        print('获取验证码请求')
        # username = request.query_params['username']
        username = request.query_params.get('username')
        user = check_user(username)
        if user:
            self.user_id = user.id
            print('验证id', self.user_id)
            gt = GeetestLib(pc_geetest_id, pc_geetest_key)
            self.status = gt.pre_process(self.user_id)
            print(27, self.status)
            response_str = gt.get_response_str()
            print(29, response_str)
            return MyResponse(200, True, response_str)
        return MyResponse(400, '用户不存在')

    def post(self, request):
        print(222222)
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        print(333333)
        uname = request.data['username']
        # if self.status:
        if uname:
            print(uname)
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
            re = {"status": "success"}
        else:
            result = gt.failback_validate(challenge, validate, seccode)
            re = {"status": "fail"}
        print(44, result)
        # result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
        # result = {"status": "success"} if result else {"status": "fail"}
        print(47, re)
        return MyResponse(re)

class CheckPhoneAPIView(APIView):
    def get(self,request,phone):
        if not re.match(r'^1[3-9][0-9]{9}', phone):
            return Response({'message':'手机格式有误'},status=400)
        try:
           user = check_user(phone)
        except:
            user = None
        if user :
            # return MyResponse(401, '手机号已被注册')
            return Response({'message':'手机号已被注册'},status=400)
        return Response({'message':'手机正确'},status=200)

class SendmessageAPIView(APIView):
    def get(self,request,*args,**kwargs):
        phone = kwargs.get('phone')
        if not phone:
            print(phone)
            return Response('手机号不能为空')
        redis_connect = get_redis_connection('sms')
        code = '%d' %random.randint(100000,999999)
        if redis_connect.get('sms_interval_%s' % phone):
            return Response('60秒内已发送过短信')
        redis_connect.setex('sms_interval_%s' % phone,60,code)
        redis_connect.setex('sms_expire_%s' % phone ,60000,code)
        try:
            sms = SMSSend('ad7362d2880d845592b1fcd591399eb9')
            sms.send_msg(phone, code)
            print(sms.send_msg(phone, code))
            print('发送成功')
            return Response({'message': '发送验证码成功'}, status=200)

        except:
            print('发送失败')
            return Response({'message': '发送验证码失败'}, status=401)



        # sms = SMSSend('ad7362d2880d845592b1fcd591399eb9')
        # sms.send_msg(phone, code)
        #
        #     print('发送成功')
        #     return Response({'message':'发送验证码成功'},status=400)
        # print('发送失败')
        # return Response({'message':'发送验证码失败'},status=200)


class RegisterCreateAPIView(CreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer

class LogoutAccountAPIView(DestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = 'username'