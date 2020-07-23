from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django_redis import get_redis_connection

# Create your views here.
from course.models import Course, CourseExpire
from utils.Response import MyResponse


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def add_cart(self, request):
        course_id = request.data.get('course_id')
        user_id = request.data.get('user_id')
        expire = 0
        print(16, course_id, user_id)
        # expire = request.data.get('expire')
        try:
            course = Course.objects.get(id=course_id, is_show=True)
        except Course.DoesNotExist:
            return Response({'message': '该课程不存在'}, status=401)
        redis_connection = get_redis_connection('cart')
        pipeline = redis_connection.pipeline()
        pipeline.multi()
        pipeline.hset('goods_%s' % user_id, course_id, expire)
        pipeline.sadd('selected_%s' % user_id, course_id)
        pipeline.execute()
        cart_length = redis_connection.hlen('goods_%s' % user_id)
        print('数量', cart_length)
        # course = redis_connection.hget('goods_%s' % user_id)
        # print(course)
        return Response({'message': '添加成功', 'cart_length': cart_length})
        # return Response({'message':'添加成功'})

    def show_cart(self, request):
        user_id = request.query_params.get('user_id')
        # print(user_id)
        redis_connection = get_redis_connection('cart')
        course_list = redis_connection.hgetall('goods_%s' % user_id)
        # print(43, course_list)
        select_list = redis_connection.smembers('selected_%s' % user_id)
        cart_length = redis_connection.hlen('goods_%s' % user_id)
        # course = redis_connection.hdel('goods_%s' % user_id)
        courses = []
        for course_byte, expire_byte in course_list.items():
            course_id = int(course_byte)
            expire_id = int(expire_byte)
            # print(47,expire_id)
            # course = Course.objects.filter(id=course_id,is_show=True,is_delete=False).values()[0]
            course = Course.objects.filter(id=course_id, is_show=True, is_delete=False)[0]
            courses.append({
                'select': True if course_byte in select_list else False,
                'name': course.name,
                'id': course.id,
                'course_img': 'http://127.0.0.1:8000/' + course.course_img.url,
                'expire_id': expire_id,
                'price': course.price,
                'expire_list': course.expire_list,
                # 'price': course.final_expire_price(expire_id) if expire_id > 0 else course.price,
                'final_expire_price': '%.2f' % course.final_expire_price(expire_id),
                'discount_name': course.discount_name
            })
            # print(course.course_img.url)
        return Response({'message': '展示成功', 'courses': courses, 'cart_length': cart_length, }, status=200)
        # return Response({'message': '展示成功'}, status=200)

    # def select_cart(self,request):
    #     # user_id = request.query_params.get('user_id')
    #     # course_id = request.query_params.get('course_id')
    #     # select = request.query_params.get('select')
    #
    #     user_id = request.data.get('user_id')
    #     course_id = request.data.get('course_id')
    #     select = request.data['select']
    #     # select =bool(select)
    #     print(user_id,course_id,select)
    #     print(type(select))
    #     redis_connection = get_redis_connection('cart')
    #     # print('选中状态',redis_connection.smembers('selected_%s' % user_id))
    #     if select :
    #         print('选中')
    #         redis_connection.sadd('selected_%s' % user_id,course_id)
    #     else:
    #         print('未选中')
    #         redis_connection.srem('selected_%s' % user_id,course_id)
    #         print('筛选后', redis_connection.smembers('selected_%s' % course_id))
    #     return Response({'message':'切换选中状态成功'})

    def del_cart(self, request):
        user_id = request.data.get('user_id')
        course_id = request.data.get('course_id')
        select = request.data['select']
        redis_connection = get_redis_connection('cart')
        print(select, type(select))
        redis_connection.hdel('goods_%s' % user_id, course_id)
        if select:
            redis_connection.srem('selected_%s' % user_id, course_id)
            # print('删除后', redis_connection.hgetall('goods_%s' % user_id))
        return MyResponse(200, {'message': '删除成功'}, )

    def select_cart(self, request):
        # user_id = request.query_params.get('user_id')
        # course_id = request.query_params.get('course_id')
        # select = request.query_params.get('select')

        user_id = request.data.get('user_id')
        course_id = request.data.get('course_id')
        select = request.data.get('select')
        redis_connection = get_redis_connection('cart')

        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except Course.DoesNotExist:
            return MyResponse(400, '切换选择状态的课程不存在')

        if select:
            redis_connection.sadd('selected_%s' % user_id, course_id)
            # select_len = redis_connection.scard('selected_%s' % user_id)
            # goods_len = redis_connection.hlen('goods_%s' % user_id)
            # print('长度', select_len, goods_len)
            # if select_len == goods_len:
            #     print('全选')
            #     select_all = True
            # else:
            #     select_all = False
        else:
            redis_connection.srem('selected_%s' % user_id, course_id)
            # print('未全选')
            # select_all = False
        return Response({'message': '切换选中状态成功'})





    # def select_all_cart(self, request):
    #     user_id = request.data.get('user_id')
    #     redis_connection = get_redis_connection('cart')
    #     course_list_byte = redis_connection.hgetall('goods_%s' % user_id)
    #     select_all = request.data.get('select_all')
    #     print(145,select_all,type(select_all))
    #     if select_all:
    #         for course_byte in course_list_byte.keys():
    #             course_id = int(course_byte)
    #             redis_connection.sadd('selected_%s' % user_id, course_id)
    #         return Response({'message': '全选'})
    #     else:
    #         # for course_byte in course_list_byte.keys():
    #         #     course_id = int(course_byte)
    #         #     redis_connection.srem('selected_%s' % user_id, course_id)
    #         return Response({'message': '全不选'})

    def course_expire(self, request):
        user_id = request.data.get('user_id')
        course_id = request.data.get('course_id')
        expire_id = request.data.get('expire_id')
        print(141, expire_id, course_id, user_id)

        course = Course.objects.filter(id=course_id, is_show=True, is_delete=False)[0]
        if expire_id > 0:
            CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)
        redis_connection = get_redis_connection('cart')
        redis_connection.hset('goods_%s' % user_id, course_id, expire_id)
        # return Response({'message': '切换有效期成功', 'final_expire_price': course.final_expire_price(expire_id)},
        #                 status=200)
        return Response({'message': '切换有效期成功', 'final_expire_price': '%.2f' % course.final_expire_price(expire_id)},
                        status=200)

    # def course_expire(self, request):
    #     user_id = request.data.get('user_id')
    #     course_id = request.data.get('course_id')
    #     expire_id = request.data.get('expire_id')
    #     print(141, expire_id, course_id, user_id)
    #
    #     try:
    #         course = Course.objects.filter(id=course_id, is_show=True, is_delete=False)[0]
    #         if expire_id > 0:
    #             expire = CourseExpire.objects.get(is_show=True, is_delete=False, id=expire_id)
    #             if not expire :
    #                 raise CourseExpire.DoesNotExist()
    #     except Course.DoesNotExist:
    #         return Response({'message':'查询的课程不存在'})
    #     redis_connection = get_redis_connection('cart')
    #     redis_connection.hset('goods_%s' % user_id, course_id, expire_id)
    #     return Response({'message': '切换有效期成功', 'final_expire_price': course.final_expire_price(expire_id)}, status=200)
    def get_billCourse(self, request):
        user_id = request.user.id
        print(user_id)
        redis_connection = get_redis_connection('cart')
        course_list = redis_connection.hgetall('goods_%s' % user_id)
        select_list = redis_connection.smembers('selected_%s' % user_id)

        cart_length = redis_connection.hlen('goods_%s' % user_id)
        bill_length = redis_connection.scard('selected_%s' % user_id)

        courses = []
        # for course_select_byte in select_list:
        total_price = 0
        for course_byte, expire_byte in course_list.items():
            course_id = int(course_byte)
            expire_id = int(expire_byte)
            # print(47,expire_id)
            # course = Course.objects.filter(id=course_id,is_show=True,is_delete=False).values()[0]
            if course_byte in select_list:

                course = Course.objects.filter(id=course_id, is_show=True, is_delete=False)[0]
                price = course.price
                expire_text = '永久有效'
                if expire_id > 0:
                    expire = CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)[0]
                    price = expire.price
                    expire_text = expire.expire_text
                courses.append({
                    'name': course.name,
                    'id': course.id,
                    'course_img': 'http://127.0.0.1:8000/' + course.course_img.url,
                    'expire_id': expire_id,
                    'expire_text': expire_text,
                    'price': price,
                    'expire_list': course.expire_list,
                    # 'price': course.final_expire_price(expire_id) if expire_id > 0 else course.price,
                    'final_expire_price': '%.2f' % course.final_expire_price(expire_id),
                    'discount_name': course.discount_name,
                    # 'active':course.active,
                })
                total_price += course.final_expire_price(expire_id)
            # print(course.course_img.url)
        return Response({'message': '获取结算课程', 'courses': courses, 'cart_length': cart_length,
                         'bill_length': bill_length, 'total_price': '%.2f' % total_price}, status=200)
        # return MyResponse(200,'获取结算课程')
