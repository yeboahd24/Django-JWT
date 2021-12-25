from django.db import models
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
import uuid



class UserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        user = self.model(
            full_name,
            email=self.normalize_email(email),
        
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, full_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(PermissionsMixin, AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "login"




class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100)
    full_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = 'profile'




class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token

    class Meta:
        db_table = 'token'