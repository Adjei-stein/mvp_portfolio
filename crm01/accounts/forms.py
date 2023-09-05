from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *


class ProdForm(ModelForm):			
	class Meta:
		model = Customization
		fields = '__all__'
		exclude = ['customization', 'customer']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)

		for field_name, field in self.fields.items():
			self.fields[field_name].widget.attrs['placeholder'] = field.label
		
class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']