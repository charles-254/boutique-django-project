from django.views.generic import TemplateView, View
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.forms import formset_factory
from django.http import JsonResponse
from django.urls import reverse_lazy
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
    def get(self, request):
        employee_id = LoginView.row[0] if LoginView.row else None
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
    print(LoginView.row, " -sales")
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

class YourProfile(LoginRequiredMixin,View):
    def get(self, request):
        employee_id = LoginView.row[0]
        employees = Employee.objects.filter(pk=employee_id)
        return render(request, 'your_profile.html', {"employees": employees})

class EditPersonalDetails(LoginRequiredMixin, View):
    def get(self, request):
        ID = LoginView.row[0]
        employee = Employee.objects.get(employee_login_id=ID)  # Assuming the employee you want to edit has id=1
        initial_data = {
            'first_name': employee.first_name,
            'second_name': employee.second_name,
            'surname': employee.surname,
            'email': employee.email,
            'phone': employee.phone,
            'address': employee.address
        }
        form = PersonalDetailsEditForm(initial_data, instance=employee, employee_identity=ID)
        return render(request, 'edit_personal_details.html', {'form': form})

    def post(self, request):
        form = PersonalDetailsEditForm(request.POST)
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        employee_id = LoginView.row[0]

        with connection.cursor() as cursor:
            cursor.execute("UPDATE paramount_employee SET first_name = %s, second_name = %s, surname = %s, email = %s, "
                           "phone = %s, address = %s WHERE employee_login_id = %s",
                           [first_name, second_name, surname, email, phone, address, employee_id])
            connection.commit()
        return redirect('your-profile')

class ChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm()
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        employee_id = LoginView.row[0]
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM paramount_employeelogin WHERE  id = %s",
                            [employee_id])
            pwd = cursor.fetchone()

        if pwd is not None:
            passwd = pwd[0]
            if old_password == passwd:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE paramount_employeelogin SET password = %s WHERE id = %s",
                                   [new_password, employee_id])
                messages.success(request, "password updated successfully")
                return redirect('your-profile')

            else:
                messages.error(request, "wrong password")
                return render(request, 'change_password.html', {'form': form})

        return render(request, 'change_password.html', {'form': form})

class ForgotPassword(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        username = request.POST.get('username')

        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM paramount_employeelogin WHERE  username = %s",
                            [username])
            un = cursor.fetchone()
            messages.success(request, f"your password is {un}")

        return redirect('login')

class Recordsales(View):
    def get(self, request):
        form = SalesForm()
        return render(request, 'record_sales.html', {'form': form})

    def post(self, request):
        form = SalesForm(request.POST)
        code = request.POST.get('code')
        price = request.POST.get('price')
        quantity_sold = request.POST.get('quantity')
        total_income = int(quantity_sold) * int(price)
        sales_date = datetime.now().strftime('%Y-%m-%d')
        employee_id = LoginView.row[0]


        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM paramount_employeelogin WHERE id = %s",
                           [employee_id])
            un =cursor.fetchone()
            username = un[0]

            cursor.execute("SELECT name FROM paramount_salesdata WHERE code = %s",
                           [code])
            nm = cursor.fetchone()
            product_name = nm[0]

            cursor.execute(
                "INSERT INTO paramount_salesdata(username,code,price,quantity,total_income,sales_date,employee_id, name) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                [username, code, price, quantity_sold, total_income, sales_date, employee_id, product_name])

            cursor.execute("SELECT quantity FROM paramount_product WHERE code = %s",
                           [code])
            qn = cursor.fetchone()
            old_quantity = qn[0]
            new_quantity = int(old_quantity) - int(quantity_sold)
            cursor.execute("UPDATE paramount_product SET quantity = %s WHERE code = %s",
                           [new_quantity, code])

            messages.success(request,"Sales recorded succesfully")  # Return success response

        return render(request, 'record_sales.html', {'form': form})

