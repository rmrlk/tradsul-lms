from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Usuário")
    role = models.CharField(max_length=150, default="Colaborador", verbose_name="Cargo")
    direct_manager = models.CharField(max_length=150, blank=True, null=True, verbose_name="Gestor Direto")
    total_hours = models.IntegerField(default=0, verbose_name="Tempo total de plataforma (Horas)")
    weekly_access_days = models.IntegerField(default=0, verbose_name="Dias de acesso na semana atual")

    def __str__(self):
        return f"Perfil: {self.user.username}"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Área/Pasta")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='subcategories',
        verbose_name="Área Pai / Pasta Mãe"
    )

    class Meta:
        verbose_name = "Área / Categoria"
        verbose_name_plural = "Áreas e Subpastas"

    def __str__(self):
        if self.parent:
            return f"{self.parent} -> {self.name}"
        return self.name


class Course(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='courses', 
        verbose_name="Área / Subpasta",
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200, verbose_name="Título do Curso")
    description = models.TextField(verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Curso")
    title = models.CharField(max_length=200, verbose_name="Título da Aula / Módulo")
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, verbose_name="Material de Estudo em PDF")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL da Videoaula (YouTube)")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Arquivo da Videoaula (Upload PC)")
    content = models.TextField(blank=True, null=True, verbose_name="Instruções ou Transcrição")
    forms_url = models.URLField(blank=True, null=True, verbose_name="Link do Simulado (Google Forms)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    @property
    def youtube_embed_url(self):
        if not self.video_url:
            return None
        url = self.video_url
        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return None


class StudentGrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades', verbose_name="Aluno")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Matéria / Assunto")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
    grade = models.FloatField(verbose_name="Nota do Simulado (0 a 10)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data do Registro")

    def __str__(self):
        return f"{self.user.username} - {self.category.name}: Nota {self.grade}"