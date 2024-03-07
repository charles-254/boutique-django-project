from django.contrib.auth.forms import AuthenticationForm
from .models import *

class EmployeeLoginForm(AuthenticationForm):
    class Meta:
        model = EmployeeLogin
        fields = ['username','password']