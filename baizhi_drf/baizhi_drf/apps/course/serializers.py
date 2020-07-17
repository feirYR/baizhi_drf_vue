from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseChapter


class CourseCategoryModelSerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id','name']

class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name','role','title','signature','image']

class  CourseModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()
    class Meta:
        model = Course
        fields = ['id','name','course_img','course_type','lessons','level','pub_lessons','students','price','lesson_list','teacher','chapter_list']
        # fields = '__all__'

class ChapterModelSerializer(ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = ['name','chapter','course','chapter_list']