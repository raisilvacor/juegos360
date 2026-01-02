"""
Comando personalizado para criar superusuário
Útil para produção quando não há acesso interativo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea un superusuario desde variables de entorno o con valores por defecto'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nombre de usuario',
            default=os.environ.get('ADMIN_USERNAME', 'admin')
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email del superusuario',
            default=os.environ.get('ADMIN_EMAIL', 'admin@juegos360.com')
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Contraseña del superusuario',
            default=os.environ.get('ADMIN_PASSWORD', 'admin123')
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username}" ya existe. No se creó.')
            )
            return

        # Crear superusuario
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superusuario creado exitosamente!\n'
                    f'Usuario: {username}\n'
                    f'Email: {email}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al crear superusuario: {str(e)}')
            )

