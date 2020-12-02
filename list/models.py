from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User

class Category(models.Model): 
     name = models.CharField(max_length=100) 
     class Meta:
         verbose_name = ("Category")
         verbose_name_plural = ("Categories")
     def __str__(self):
         return self.name #name to be shown when called


# Create your models here.
class MyList(models.Model):
	title=models.CharField(max_length=100) 
	details=models.TextField(blank=True) 
	created_at = models.DateTimeField(default=timezone.now)
	status = models.BooleanField(default=False)
	category = models.ForeignKey(Category, default='general', on_delete=models.CASCADE)

	def __str__(self):
		return self.title
