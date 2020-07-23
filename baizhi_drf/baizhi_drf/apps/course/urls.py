from django.urls import path
from course import views
urlpatterns=[
    path('categories/',views.CourseCategoryListAPIView.as_view()),
    path('courses/',views.CourseListAPIView.as_view()),
    path('courses_filter/',views.CourseFilterAPIVIew.as_view()),
    path('course_detail/<str:id>',views.CourseDetailAPIView.as_view()),
    path('review/',views.ReviewViewSet.as_view({'post':'commit_review','get':'show_review'}))
]