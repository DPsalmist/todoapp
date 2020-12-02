from django import forms 
from .models import MyList

class TodoForm(forms.ModelForm): 
	class Meta: 
		model = MyList 
		fields="__all__"