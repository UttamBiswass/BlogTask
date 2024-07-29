
from django.db import models
from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user( self, email, password=None, is_staff=False, is_active=True, is_superuser=False, **extra_fields ):

        """Create a user instance with the given email and password."""
        
        email = UserManager.normalize_email(email)
        extra_fields.pop("username", None)
        user = self.model(email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser ,**extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user( email, password, is_staff=True, is_superuser=True, **extra_fields )
    
    
    
class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True,default="Admin")
    last_name = models.CharField(max_length=100, blank=True,)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ("email",)

    def __str__(self):
        return self.email

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=200, blank=True,)
    description=models.TextField(blank=True,null=True)
    post_at=models.DateTimeField(_('date started'), default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)  # Add tags field


    def __str__(self):
        return self.title
    

    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Allow nulls
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.blog.title}'

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blog', 'user')

    def __str__(self):
        return f'Like by {self.user.first_name} on {self.blog.title}'
    
