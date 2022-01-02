from django.urls import path
from . import views

app_name='oursystem'
urlpatterns = [
    path('', views.SubjectListView.as_view(), name='subject_list'),
    path('<slug:slug>/', views.CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<str:subject>/<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<str:subject>/<slug:slug>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<str:subject>/<slug:slug>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
]
