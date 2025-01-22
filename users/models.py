from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings


class UserManager(BaseUserManager):
    """
    A blueprint to create a user
    """
    def create_user(self, username, email, phone_number, password, **kwargs):
        """
        A method to create a user
        """
        if not username:
            raise ValidationError("Username Field Must Be Provided")
        if not email:
            raise ValidationError("Email Field Must Be Provided")
        if not phone_number:
            raise ValidationError("Phone Number Field Must Be Provided")
        if not password:
            raise ValidationError("Password Field Must Be Provided")
        
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, password=password, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
    def create_superuser(self, username, email, phone_number, password, **kwargs):
        """
        A method to create a superuser
        """
        
        if not username:
            raise ValidationError("UserName Field Must Be Provided")
        if not email:
            raise ValidationError("Email Must Be Provided")
        if not phone_number:
            raise ValidationError("Phone Number Field Must Be Provided")
        if not password:
            raise ValidationError("Password Field Must Be Provided")
        
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, password=password, **kwargs)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=256, db_index=True, unique=True)
    first_name = models.CharField(max_length=256, db_index=True, blank=True)
    last_name = models.CharField(max_length=256, db_index=True, blank=True)
    phone_number = PhoneNumberField(unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, max_length=100, db_index=True)
    image = models.ImageField(upload_to='users_images', blank=True)
    about = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    
    
    @property
    def name(self):
        return f"{self.first_name} {self.username}"
    
    
    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            output = BytesIO()
            width, height = 100, 100
            img = img.resize((width, height))
            img_format = img.format  # Get the original image format
            if not img_format:  # If format is None, default to JPEG
                img_format = 'JPEG'
                img.save(output, format=img_format)
                output.seek(0)
                self.image = ContentFile(output.getvalue(), name=self.image.name)
        super().save(*args, **kwargs)
        
     
    
    def get_user_image(self):
        if self.image:
            return self.image.url
        else:
            return settings.MEDIA_URL + "usersimage.jpg"
            
            
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']
    
    
    objects = UserManager()
    
    
    