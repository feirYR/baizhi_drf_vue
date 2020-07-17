from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from django_redis import get_redis_connection

# Create your views here.
from course.models import Course
from utils.Response import MyResponse


class CartViewSet(ViewSet):

    def add_cart(self, request):
        course_id = request.data.get('course_id')
        user_id = request.data.get('user_id')
        expire = 0
        print(16,course_id,user_id)
        # expire = request.data.get('expire')
        try:
            Course.objects.get(id=course_id,is_show=True)
        except Course.DoesNotExist:
            return Response({'message': '该课程不存在'}, status=401)

        redis_connection = get_redis_connection('cart')
        pipeline = redis_connection.pipeline()
        pipeline.multi()
        pipeline.hset('goods_%s' % user_id,course_id,expire)
        pipeline.sadd('selected_%s' % user_id,course_id)
        pipeline.execute()
        cart_length = redis_connection.hlen('goods_%s' % user_id)
        print('数量',cart_length)
        # course = redis_connection.hget('goods_%s' % user_id)
        # print(course)
        return Response({'message':'添加成功','cart_length':cart_length})
        # return Response({'message':'添加成功'})

    def show_cart(self,request):
        user_id = request.query_params.get('user_id')
        # print(user_id)
        redis_connection = get_redis_connection('cart')
        course_list = redis_connection.hgetall('goods_%s' % user_id)
        select_list =redis_connection.smembers('selected_%s' % user_id)
        cart_length = redis_connection.hlen('goods_%s' % user_id)
        # course = redis_connection.hdel('goods_%s' % user_id)
        courses = []
        for course_byte,expire_byte in course_list.items():
            course_id = int(course_byte)
            expire_id = int(expire_byte)
            # print(47,expire_id)
            # course = Course.objects.filter(id=course_id,is_show=True,is_delete=False).values()[0]
            course = Course.objects.filter(id=course_id,is_show=True,is_delete=False)[0]
            courses.append({
                'select':True if course_byte in select_list else False,
                'name':course.name,
                'id':course.id,
                'course_img':'http://127.0.0.1:8000/'+course.course_img.url,
                'expire':expire_id,
                'price':course.price,
            })
            # print(course.course_img.url)
        return Response({'message': '展示成功','courses':courses,'cart_length': cart_length,}, status=200)
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

    def del_cart(self,request):
        user_id = request.data.get('user_id')
        course_id = request.data.get('course_id')
        select = request.data['select']
        print(user_id, course_id, select)
        redis_connection = get_redis_connection('cart')
        # if select == 'true':
        if select :
            redis_connection.hdel('goods_%s' % user_id ,course_id)
        else:
            return MyResponse(400, {'message': '选中后才可删除'}, )
        print('删除后', redis_connection.hgetall('goods_%s' % user_id))
        return MyResponse(200, {'message': '删除成功'}, )


    def select_cart(self,request):
        # user_id = request.query_params.get('user_id')
        # course_id = request.query_params.get('course_id')
        # select = request.query_params.get('select')

        user_id = request.data.get('user_id')
        course_id = request.data.get('course_id')
        select = request.data['select']
        redis_connection = get_redis_connection('cart')
        if course_id:
            # select =bool(select)
            print(user_id,course_id,select)
            print(type(select))

            # print('选中状态',redis_connection.smembers('selected_%s' % user_id))
            if select :
                print('选中')
                redis_connection.sadd('selected_%s' % user_id,course_id)
            else:
                print('未选中')
                redis_connection.srem('selected_%s' % user_id,course_id)
                print('筛选后', redis_connection.smembers('selected_%s' % course_id))
        else:
            if select:
                course_list_byte = redis_connection.hgetall('goods_%s' % user_id)
                for course_byte in course_list_byte.keys():
                    print('全选',course_byte)
                    course_id = int(course_byte)
                    print('全选', course_id)
                    redis_connection.sadd('selected_%s' % user_id, course_id)
                return Response({'message': '切换全选状态成功','select_all':True})

        return Response({'message':'切换选中状态成功'})