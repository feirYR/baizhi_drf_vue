from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from baizhi_drf.libs.geetest import GeetestLib
from user.utils import check_user
from utils.Response import MyResponse

pc_geetest_id = "6f91b3d2afe94ed29da03c14988fb4ef"
pc_geetest_key = "7a01b1933685931ef5eaf5dabefd3df2"

class Captche(APIView):
    user_id = 0
    status = False
    def get(self,request):
        print('获取验证码请求')
        # username = request.query_params['username']
        username = request.query_params.get('username')
        print(1111)
        user=check_user(username)
        if user:
            self.user_id = user.id
            print('验证id', self.user_id)
            gt = GeetestLib(pc_geetest_id, pc_geetest_key)
            self.status = gt.pre_process(self.user_id)

            response_str = gt.get_response_str()
            print(27,response_str)
            return MyResponse(response_str)
        return MyResponse(400,'用户不存在')

    def post(self,request):
            print(222222)
            gt = GeetestLib(pc_geetest_id, pc_geetest_key)
            challenge = request.POST.get(gt.FN_CHALLENGE, '')
            validate = request.POST.get(gt.FN_VALIDATE, '')
            seccode = request.POST.get(gt.FN_SECCODE, '')
            # if self.status:
            if self.user_id :
                result = gt.success_validate(challenge, validate, seccode,  self.user_id)
            else:
                result = gt.failback_validate(challenge, validate, seccode)
            # result = "<html><body><h1>登录成功</h1></body></html>" if result else "<html><body><h1>登录失败</h1></body></html>"
            result = {"status": "success"} if result else {"status": "fail"}
            return MyResponse(result)
