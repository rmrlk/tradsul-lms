import os
import django

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
master_email = 'arthur.romao@tradsul.com.br'
master_pass = 'Romao2120@'

# Garante que as migrações já ocorreram antes de interagir com a tabela
try:
    user = User.objects.filter(username=master_email).first() or User.objects.filter(email=master_email).first()
    if user:
        user.username = master_email
        user.email = master_email
        user.set_password(master_pass)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"SUCCESS: Usuario Master {master_email} atualizado com sucesso!")
    else:
        User.objects.create_superuser(username=master_email, email=master_email, password=master_pass)
        print(f"SUCCESS: Usuario Master {master_email} criado com sucesso!")
except Exception as e:
    print(f"ERROR ao criar usuario Master: {e}")