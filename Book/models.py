from django.db import models
from User.models import User

# Create your models here.
class Book(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    best_seller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    num_pages = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    