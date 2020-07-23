import os
from datetime import datetime

from alipay import AliPay
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from baizhi_drf import settings
from django.conf import settings
from baizhi_drf.settings.develop import BASE_DIR
from course.models import CourseExpire
from order.models import Order
from utils.Response import MyResponse


class AlipayAPIView(APIView):

    def get(self, request):

        order_number = request.query_params.get('order_number')
        print(order_number)
        try:
            order = Order.objects.get(order_number=order_number)
            print(order)
        except Order.DoesNotExist:
            return MyResponse(400, '请求的订单不存在')

        # 初始化支付参数
        app_private_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read()
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],  # 沙箱支付的id
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG["debug"],  # 默认False
        )

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # 生成支付的链接地址
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,
            total_amount=float(order.real_price),
            subject=order.order_title,
            return_url=settings.ALIAPY_CONFIG["return_url"],
            notify_url=settings.ALIAPY_CONFIG['notify_url'],  # 可选, 不填则使用默认notify url

        )

        url = settings.ALIAPY_CONFIG['gateway_url'] + order_string
        # return MyResponse(200,'返回支付页面',url)
        return Response(url)


class AlipayResultAPIView(APIView):

    def get(self, request):
        # 初始化支付参数
        app_private_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(BASE_DIR, "apps/payments/keys/app_private_key.pem")).read()
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG["appid"],  # 沙箱支付的id
            app_notify_url=settings.ALIAPY_CONFIG["app_notify_url"],  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type=settings.ALIAPY_CONFIG["sign_type"],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG["debug"],  # 默认False
        )
        # 验证支付结果
        data = request.query_params.dict()
        print('支付结果', data)
        signature = data.pop("sign")
        success = alipay.verify(data, signature)
        success = True
        if success:
            return self.payResult(data)
        return Response({'message': '验证支付结果失败'})

    def payResult(self, data):
        print(11111111111111)
        out_trade_no = data.get('out_trade_no')
        print(out_trade_no)
        order = Order.objects.filter(order_number=out_trade_no)[0]
        order.pay_time = datetime.now()
        order.order_status = 1
        order_detail_list = order.order_courses.all()
        # with transaction.atomic():
        rollbake_point = transaction.savepoint()
        # try:
        course_list = []
        for order_detail in order_detail_list:
            course = order_detail.course
            # course_list.append(course)
            course.students += 1
            course.save()

            expire_id = order_detail.expire

            if expire_id > 0:
                expire = CourseExpire.objects.filter(id=expire_id)[0]
                expire_time = expire.expire_time * 24 * 3600
                print('有效期', expire_time)
                out_time = datetime.fromtimestamp(order.pay_time + expire_time)
            else:
                out_time = None
            course_list.append({
                'course_id':course.id,
                'course_name': course.name,
                'out_time': out_time,
                'studens': course.students,

            })
            print('购买课程列表', course_list)
        # except:
        # transaction.savepoint_rollback(rollbake_point)
        # return Response({'message':'创建课程购买记录失败'},status=400)

        return Response({
            'message': '创建课程购买记录成功',
            'course_list': course_list,
            'course_len': order_detail_list.count(),
            # 'course_len': len(course_list),
            'butype': order.pay_type,
            'pay_time': datetime.now(),
            'real_price': order.real_price,
        }, status=200)
