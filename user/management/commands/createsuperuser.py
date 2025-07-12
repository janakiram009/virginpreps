# user/management/commands/createsuperuser.py

from django.core.management.base import CommandError
from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser with phone number as the unique identifier.'

    def add_arguments(self, parser):
        parser.add_argument('--phone_number', required=True, help='Phone number of the superuser')
        parser.add_argument('--password', help='Optional password for the superuser')

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        password = options.get('password')

        if UserModel.objects.filter(phone_number=phone_number).exists():
            raise CommandError('Superuser with this phone number already exists.')

        user_data = {
            'phone_number': phone_number,
            'is_staff': True,
            'is_superuser': True,
        }

        if password:
            user = UserModel.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
        else:
            # Let Django prompt for password
            user = UserModel.objects.create_superuser(phone_number=phone_number)

        self.stdout.write(self.style.SUCCESS(f"Superuser created successfully with phone: {phone_number}"))
