from django.contrib import admin
from .models import MyList, Category

# Register your models here.
admin.site.register(Category)

@admin.register(MyList)
class MyListAdmin(admin.ModelAdmin):
	list_display  = ['title', 'created_at', 'status']
	search_fields = ['title']