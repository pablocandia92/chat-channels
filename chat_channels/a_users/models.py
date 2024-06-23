from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, phone, password=None, **extra_fields):
        email = self.normalize_email(email)

        if User.objects.filter(email=email).exists():
            raise ValueError('El Email ya ha sido registrado')
        
        # elif User.objects.filter(phone=phone).exists():
        #     raise ValueError('Phone alredy register')
        
        user = self.model(email=email, full_name=full_name, phone=phone, **extra_fields)

        if password:
            user.set_password(password)
        else:
            raise ValueError('La contraseña es obligatoria')
        
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
   
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']

    def __str__(self):
        return self.email