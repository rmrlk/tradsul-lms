from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Course, Category, Lesson

# Verificação se o usuário é o Master/CEO
def is_master(user):
    return user.is_authenticated and user.is_superuser

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Autenticação utilizando o e-mail corporativo como username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')

    return render(request, 'courses/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def student_dashboard(request):
    courses = Course.objects.all()
    categories = Category.objects.all()
    return render(request, 'courses/student_dashboard.html', {
        'courses': courses,
        'categories': categories
    })

@user_passes_test(is_master)
def admin_dashboard(request):
    users = User.objects.all()
    courses = Course.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Ação: Criar novo membro da equipe
        if action == 'create_user':
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name', '')
            
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Usuário com este e-mail já existe.')
            else:
                User.objects.create_user(username=email, email=email, password=password, first_name=first_name)
                messages.success(request, f'Membro {email} cadastrado com sucesso!')
                return redirect('admin_dashboard')

        # Ação: Excluir membro
        elif action == 'delete_user':
            user_id = request.POST.get('user_id')
            user_to_delete = get_object_or_404(User, id=user_id)
            if not user_to_delete.is_superuser:
                user_to_delete.delete()
                messages.success(request, 'Membro removido com sucesso.')
            else:
                messages.error(request, 'Não é possível remover o usuário Master.')
            return redirect('admin_dashboard')

    return render(request, 'courses/admin_dashboard.html', {
        'users': users,
        'courses': courses
    })

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lessons.all()
    return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons})

@login_required
def category_grid(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    courses = Course.objects.filter(category=category)
    return render(request, 'courses/category_grid.html', {'category': category, 'courses': courses})