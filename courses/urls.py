from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Navegação de Cursos
    path('', views.category_view, name='category_home'),
    path('area/<int:category_id>/', views.category_view, name='category_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Painéis
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('meu-desempenho/', views.student_dashboard, name='student_dashboard'),
    path('aluno/<int:student_id>/', views.student_dashboard, name='student_detail'),
]