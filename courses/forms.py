from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class StudentSignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label="Nome", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seu Nome'}))
    last_name = forms.CharField(max_length=50, label="Sobrenome", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seu Sobrenome'}))
    email = forms.EmailField(label="E-mail Corporativo (@tradsul.com.br)", widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'seu.nome@tradsul.com.br'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Escolha sua senha'}), label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirme sua senha'}), label="Confirmar Senha")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not email.endswith('@tradsul.com.br'):
            raise ValidationError("Apenas e-mails do domínio @tradsul.com.br são permitidos para cadastro.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail corporativo já está cadastrado no sistema.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")