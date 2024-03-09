from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import *

class EmployeeLoginForm(AuthenticationForm):
    class Meta:
        model = EmployeeLogin
        fields = ['username','password']

class PersonalDetailsEditForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'second_name', 'surname', 'email', 'phone', 'address']

    def __init__(self, *args, employee_identity=None, **kwargs):
        self.employee_identity = employee_identity
        super(PersonalDetailsEditForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Employee.objects.exclude(employee_login_id=self.employee_identity).filter(email=email).exists():
            raise forms.ValidationError("Employee with this Email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Employee.objects.exclude(employee_login_id=self.employee_identity).filter(phone=phone).exists():
            raise forms.ValidationError("Employee with this Phone already exists.")
        return phone

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=65,)