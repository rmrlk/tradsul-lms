from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Category, Course, Lesson, StudentGrade, UserProfile
from .forms import StudentSignUpForm

# View de Cadastro
def register_view(request):
    if request.user.is_authenticated:
        return redirect('category_home')
        
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            # Cria o usuário normal (is_staff=False por padrão -> Aluno)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Cria o perfil do colaborador
            UserProfile.objects.get_or_create(user=user, role="Colaborador")
            
            login(request, user)
            return redirect('category_home')
    else:
        form = StudentSignUpForm()
        
    return render(request, 'courses/register.html', {'form': form})


# View de Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('category_home')

    error_message = None
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('category_home')
        else:
            error_message = "E-mail ou senha incorretos. Verifique suas credenciais."

    return render(request, 'courses/login.html', {'error_message': error_message})


# View de Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Páginas Restritas
@login_required
def category_view(request, category_id=None):
    current_category = None
    subcategories = []
    courses = []

    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        subcategories = current_category.subcategories.all()
        courses = current_category.courses.all()
    else:
        subcategories = Category.objects.filter(parent__isnull=True)

    context = {
        'current_category': current_category,
        'subcategories': subcategories,
        'courses': courses,
    }
    return render(request, 'courses/category_grid.html', context)


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})


# PROTEÇÃO: Apenas Usuários is_staff = True entram aqui
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        # Se for aluno comum, redireciona para a página principal de cursos
        return redirect('category_home')

    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    
    users_data = User.objects.annotate(avg_grade=Avg('grades__grade'))

    context = {
        'total_users': total_users,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'users_data': users_data,
    }
    return render(request, 'courses/admin_dashboard.html', context)


@login_required
def student_dashboard(request, student_id=None):
    # Se for informado um id de outro aluno e QUEM ESTÁ ACESSANDO NÃO É ADMIN, bloqueia
    if student_id and student_id != request.user.id and not request.user.is_staff:
        return redirect('student_dashboard')

    if student_id:
        user = get_object_or_404(User, id=student_id)
    else:
        user = request.user

    profile, _ = UserProfile.objects.get_or_create(user=user)
    overall_avg = StudentGrade.objects.filter(user=user).aggregate(Avg('grade'))['grade__avg'] or 0.0

    subject_grades = (
        StudentGrade.objects.filter(user=user)
        .values('category__name')
        .annotate(avg_grade=Avg('grade'))
    )

    best_subject_query = (
        StudentGrade.objects.filter(user=user)
        .values('category__name')
        .annotate(avg_grade=Avg('grade'))
        .order_by('-avg_grade')
        .first()
    )

    context = {
        'user_student': user,
        'profile': profile,
        'overall_avg': round(overall_avg, 1),
        'subject_grades': subject_grades,
        'best_subject': best_subject_query['category__name'] if best_subject_query else "Sem registros",
    }
    return render(request, 'courses/student_dashboard.html', context)