from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *

class EmployeeLoginForm(AuthenticationForm):
    class Meta:
        model = EmployeeLogin
        fields = ['username','password']

class PersonalDetailsEditForm(forms.ModelForm):

    username = models.CharField(max_length=25) #creating a username field
    class Meta:
        model = Employee
        fields = ['first_name', 'second_name', 'surname', 'email', 'phone', 'national_ID',
                  'address']

        def __init__(self, *args, **kwargs):
            super(PersonalDetailsEditForm,self).__init__(*args, **kwargs)
            if self.instance.employee_login:
                self.fields['username'].initial = self.instance.employee_login.username