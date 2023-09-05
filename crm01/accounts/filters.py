import django_filters
from django_filters import CharFilter

from .models import *

class CustomizationFilter(django_filters.FilterSet):
	customization = CharFilter(field_name='customization', lookup_expr='icontains')

	class Meta:
		model = Customization
		fields = '__all__'
		exclude = ['customization', 'customer']


class ProductFilter(django_filters.FilterSet):
	class Meta:
		model = Customization
		fields = '__all__'
		exclude = ['customization', 'customer']