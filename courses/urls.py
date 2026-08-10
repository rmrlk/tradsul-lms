from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('category/<str:category_name>/', views.category_grid, name='category_grid'),
]