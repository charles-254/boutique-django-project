from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import *
from django import forms

admin.site.site_header = "PARAMOUNT WEARS - Administration"
admin.site.site_index_title = 'Welcome to Paramount Wears Admin Portal'
admin.site.unregister(Group)
admin.site.register(Employee)


class EmployeeLoginForm(forms.ModelForm):
    class Meta:
        model = EmployeeLogin
        fields = '__all__'

    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label='User')

class EmployeeLoginAdmin(admin.ModelAdmin):
    form = EmployeeLoginForm

    def save_model(self, request, obj, form, change):
        user = form.cleaned_data['user']
        obj.save()
        obj.user = user
        obj.save()

admin.site.register(EmployeeLogin, EmployeeLoginAdmin)

class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'code','quantity','price', 'total_income', 'sales_date')  # Specify the fields to display in the list view
    list_filter = ('username', 'sales_date','code','quantity')  # Add filters
    search_fields = ('code', 'sales_date','username')  # Add search functionality

admin.site.register(SalesData, SalesDataAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code','name','price','quantity')
    list_filter = ('code', 'name')
    search_fields = ('code', 'name')

admin.site.register(Product, ProductAdmin)