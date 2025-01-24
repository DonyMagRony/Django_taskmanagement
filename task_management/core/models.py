from django.db import models 
from django.contrib.auth.models import AbstractUser 
 
from django.conf import settings
class User(AbstractUser): 
    ROLE_CHOICES = [ 

            ('admin', 'Admin'), 

            ('manager', 'Manager'), 

            ('employee', 'Employee'), 

        ] 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee') 
    first_name = models.CharField(max_length=50) 

    last_name = models.CharField(max_length=50) 

    email = models.EmailField(unique=True) 

    def save(self, *args, **kwargs):
        # Hash the password if it's set and not hashed yet
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

 

    def __str__(self): 

        return f"{self.first_name} {self.last_name}" 

 

class Project(models.Model): 

    name = models.CharField(max_length=100) 

    description = models.TextField() 

    start_date = models.DateField() 

    end_date = models.DateField() 

 

    def __str__(self): 

        return self.name 

 

class Category(models.Model): 

    name = models.CharField(max_length=100) 

 

    def __str__(self): 

        return self.name 

 

class Priority(models.Model): 

    level = models.CharField(max_length=50) 

 

    def __str__(self): 

        return self.level 

 

class Task(models.Model): 

    title = models.CharField(max_length=200) 

    description = models.TextField() 

    project = models.ForeignKey(Project, on_delete=models.CASCADE) 

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) 

    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True) 

    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) 

    due_date = models.DateField() 

 

    def __str__(self): 

        return self.title 