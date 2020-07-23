from datetime import datetime

from django.db import transaction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from course.models import Course, CourseExpire
from order.models import Order, OrderDetail
from django_redis import get_redis_connection


class OrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        # fields = '__all__'
        fields = ['id', 'order_number', 'pay_type', 'total_price', 'real_price']

        extra_kwargs = {
            'id': {'read_only': True},
            'pay_type': {'write_only': True},
            'order_number': {'read_only': True}
        }

    def validate(self, attrs):
        pay_type = attrs.get('pay_type')
        user_id = attrs.get('user_id')
        print(25,pay_type,user_id)

        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError('支付方式错误')
        return attrs

    def create(self, validated_data):
        print(1111111)
        user_id = self.context['request'].user.id
        # user_id = validated_data.get('user_id')
        # pay_type = validated_data.get('pay_type')
        # pay_type=self.validate().get('pay_type')
        # print(40,pay_type)
        # user_id = validated_data.get('user_id')
        # pay_type = validated_data.get('pay_type')

        print(35,user_id)
        # user_id = 47
        redis_connection = get_redis_connection('cart')
        incr = redis_connection.incr('order_num')
        order_number = datetime.now().strftime('%Y%m%d%H%M%S') + '%06d' % user_id + '%06d' % incr
        # print(order_number)
        order = Order.objects.create(
            order_number=order_number,
            order_title='百知课程',
            total_price=0,
            real_price=0,
            order_status=0,
            pay_type=validated_data.get('pay_type'),
            credit=100,
            coupon=1,
            order_desc='DFR,vue',
            user_id=user_id,
        )
        course_list = redis_connection.hgetall('goods_%s' % user_id)
        select_list = redis_connection.smembers('selected_%s' % user_id)

        with transaction.atomic():
            rollback_id = transaction.savepoint()

            for course_byte, expire_byte in course_list.items():
                course_id = int(course_byte)
                expire_id = int(expire_byte)
                # print(47,expire_id)
                # course = Course.objects.filter(id=course_id,is_show=True,is_delete=False).values()[0]
                if course_byte in select_list:
                    course = Course.objects.filter(id=course_id, is_show=True, is_delete=False)[0]
                    price = course.price
                    if expire_id > 0:
                        expire = CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)[0]
                        price = expire.price
                    try:
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=price,
                            real_price='%.2f' % course.final_expire_price(expire_id),
                            discount_name=course.discount_name
                            # discount_name=course.discount_name if course.active() else None
                        )
                    except:
                        transaction.savepoint_rollback(rollback_id)
                        raise serializers.ValidationError('生成订单失败')
                    order.real_price += course.final_expire_price(expire_id)
                    order.total_price += price

        order.save()
        return order
