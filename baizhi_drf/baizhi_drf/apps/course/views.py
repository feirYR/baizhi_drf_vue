from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from course.models import CourseCategory, Course
# Create your views here.
from course.serializers import CourseCategoryModelSerializer, CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from course.pagination import CoursePageNumber

class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True,is_delete=False).order_by('ordering')
    serializer_class = CourseCategoryModelSerializer

class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by('ordering')
    serializer_class = CourseModelSerializer

class CourseFilterAPIVIew(ListAPIView):
    queryset = Course.objects.filter(is_show=True,is_delete=False).order_by('ordering')
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