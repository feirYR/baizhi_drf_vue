from datetime import datetime


from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.response import Response
from django_redis import get_redis_connection
from course.models import CourseCategory, Course
# Create your views here.
from course.serializers import CourseCategoryModelSerializer, CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from course.pagination import CoursePageNumber
from rest_framework.viewsets import ViewSet




class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True,is_delete=False).order_by('ordering')
    serializer_class = CourseCategoryModelSerializer

class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by('ordering')
    serializer_class = CourseModelSerializer

class CourseFilterAPIVIew(ListAPIView):
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by('-ordering','-id')
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filter_fields = ('course_category',)
    ordering_fields=('id','students','price')
    pagination_class = CoursePageNumber

class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by('ordering')
    serializer_class = CourseModelSerializer
    lookup_field = 'id'

class ChapterAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by('ordering')
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('course')

class ReviewViewSet(ViewSet):

    def commit_review(self,request):

        user_id = request.data.get('user_id')
        course_id = request.data.get('course_id')
        review = request.data.get('review')
        datatime = datetime.now()
        redis_connection = get_redis_connection('review')
        pipeline = redis_connection.pipeline()

        pipeline.multi()
        # pipeline.hset('review_%s' % user_id,course_id,review)
        # from my_task.review.tasks import commit_review
        # commit_review.delay(course_id, review,pipeline)
        pipeline.lpush('review_%s' % course_id, review)
        # pipeline.hset('review_%s' % course_id,review,datatime)
        pipeline.execute()


        print(user_id,course_id,review)
        return Response({'message':'提交评论成功'})

    def show_review(self,request):
        user_id = request.query_params.get('user_id')
        course_id = request.query_params.get('course_id')
        redis_connection = get_redis_connection('review')
        review = redis_connection.lrange('review_%s' % course_id,0,-1)
        # print('评论',review)
        # from celery import result
        from celery.result import AsyncResult
        from my_task.main import app

        # result=show_review.delay(course_id)
        # print('执行结果', result)
        # task_id = result.task_id
        # # res = AsyncResult(resul)  # 参数为task id
        # res = AsyncResult(id=task_id,app=app)  # 参数为task id
        # status=res.state
        # review = res.get()
        # review=res.result
        # data = result.get()
        # print('状态',status)
        # print('异步结果',result)
        return Response({'message':'获取评论成功','review':review})
        # return Response({'message':'获取评论成功'})
