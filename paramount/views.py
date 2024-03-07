from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from .forms import *

class Index(TemplateView):
    template_name = 'index.html'

class LoginView(View):
    row = None
    username = None
    def get(self, request):
        form = EmployeeLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = EmployeeLoginForm(request.POST)
        LoginView.username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM paramount_employeelogin WHERE username = %s AND password = %s",
                            [LoginView.username, password])
            LoginView.row = cursor.fetchone() #we get a tuple containing the employee_id
            print(LoginView.row ," -loginview")
        if LoginView.row is not None:
            employee_id = int(LoginView.row[0])
            try:
                employee = Employee.objects.get(pk=employee_id)
                user = User.objects.get(username=employee.employee_login.username)
                login(request, user)
                return redirect('dashboard')
            except (Employee.DoesNotExist, User.DoesNotExist):
                messages.error(request,"Make sure your logins are correct")

        return render(request, 'login.html', {'form': form})

class Dashboard(LoginRequiredMixin, View):
    print(LoginView.row , " -dashboard")
    def get(self, request):
        employee_id = LoginView.row[0] if LoginView.row else None
        print(employee_id)
        if employee_id:
            employees = Employee.objects.filter(pk=employee_id)
            products = Product.objects.all().order_by('id')
            return render(request, 'dashboard.html', {"employees": employees, "products": products})
        else:
            return redirect('login')

class Products(View):
    def get(self, request):
        print("entered the get function")
        products = Product.objects.all().order_by('id')
        print("gotten the products")
        return render(request, 'products.html', {"products":products})

class SalesDataView(LoginRequiredMixin,View):
    print(LoginView.row , " -sales")
    def get(self, request):
        employee_id = LoginView.row[0]
        sales_data = SalesData.objects.filter(employee_id=employee_id).order_by('-sales_date')
        return render(request, 'sales_data.html', {'sales_data': sales_data})



def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@login_required
def Search_view(request):
    query = request.GET.get('q', None)
    employee_id = LoginView.row[0]
    queryset = None
    if query:
        if is_valid_date(query):
            # Query is a valid date, filter by sales_date
            queryset = SalesData.objects.filter(employee_id=employee_id,sales_date=query).order_by('-sales_date')
        else:
            # Query is not a valid date, filter by code
            queryset = SalesData.objects.filter(employee_id=employee_id,code=query)
    else:
        pass

    context = {
        'objects': queryset
    }
    return render(request, 'search.html', context)
