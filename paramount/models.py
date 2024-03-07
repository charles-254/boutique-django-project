from django.db import models
from django.core.validators import RegexValidator

class EmployeeLogin(models.Model):
    username = models.CharField(max_length=25,null=False, blank=False, unique=True)
    password = models.CharField(max_length=65,default='1234',null=False, blank=False)


    def __str__(self):
        return f"EmployeeLogin username ({self.username }) id ({self.pk})"

class Employee(models.Model):
    national_ID = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(unique=True)
    address = models.CharField(max_length=100)
    user_role = models.CharField(max_length=25)
    salary = models.IntegerField()
    commission = models.IntegerField(default=0)
    employee_login = models.OneToOneField(EmployeeLogin, on_delete=models.CASCADE, primary_key=True)


    def __str__(self):
        return f"Employee first name ({self.first_name }) id ({self.pk})"

class Product(models.Model):
    code = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=25, unique=True)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"Product code ({self.code})"

class SalesData(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    username = models.CharField(max_length=25)
    code = models.CharField(max_length=25)
    price = models.IntegerField()
    quantity = models.IntegerField()
    total_income = models.IntegerField()
    date_format_validator = RegexValidator(
        regex=r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD format
        message='Date must be in the format YYYY-MM-DD',
        code='invalid_date_format'
    )
    sales_date = models.DateField(validators=[date_format_validator])
