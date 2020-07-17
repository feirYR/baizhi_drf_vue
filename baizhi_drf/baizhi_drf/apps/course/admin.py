from django.contrib import admin
from course.models import Course,CourseCategory,CourseChapter,CourseLesson,Teacher,CourseDiscountType,CourseDiscount,CourseExpire,CoursePriceDiscount,Activity
# Register your models here.
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CourseChapter)
admin.site.register(CourseLesson)
admin.site.register(Teacher)
admin.site.register(CourseDiscountType)
admin.site.register(CourseDiscount)
admin.site.register(CoursePriceDiscount)
admin.site.register(Activity)
admin.site.register(CourseExpire)