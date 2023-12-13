from django.shortcuts import render, redirect
from django import forms
from employee.apps import EmployeeConfig
from employee.forms import EmployeeForm
from django.http import HttpResponse
from openpyxl import Workbook
from employee.models import Employee
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.urls import reverse_lazy
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
# from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import csv
from django.conf import settings
from django.core.mail import send_mail
import threading
from threading import Thread
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from employee.models import Employee



def bulk_create_from_data(request):
    employee = [
        {'eid': '5', 'ename': 'John Doe', 'eemail': 'john@example.com', 'ephone': '1234567890', 'eage': 30},
        {'eid': '22', 'ename': 'Jane Doe', 'eemail': 'jane@example.com', 'ephone': '9876543210', 'eage': 25},
        {'eid': '8', 'ename': 'Jon', 'eemail': 'jon@example.com', 'ephone': '852741963322', 'eage':24 },
        {'eid': '28', 'ename': 'Joan', 'eemail': 'jofv bn@example.com', 'ephone': '8627419689322', 'eage':21 },
        {'eid': '38', 'ename': 'ton', 'eemail': 'jodcvn@example.com', 'ephone': '852741963322', 'eage':24 },        
        {'eid': '48', 'ename': 'Non', 'eemail': 'josedn@example.com', 'ephone': '852741963722', 'eage':24 },
        {'eid': '18', 'ename': 'Oon', 'eemail': 'jodsn@example.com', 'ephone': '852741963342', 'eage':24 },
        {'eid': '2', 'ename': 'pan', 'eemail': 'jodn@example.com', 'ephone': '8527419675322', 'eage':24 },
        {'eid': '27', 'ename': 'pan', 'eemail': 'joasdfgdn@example.com', 'ephone': '852741956252675322', 'eage':24 },
     ]
    employees_to_create = [Employee(**data) for data in employee]
    print ('Employees to create', employees_to_create)
    try:
        employees_to_create = [Employee(**data) for data in employee]
        Employee.objects.bulk_create(employees_to_create)
        return HttpResponse("Bulk create successful!")
    except Exception as e:
        return HttpResponse(f"Error during bulk create: {e}")

    # return render(request, 'home.html')


def send_bulk_create_email_async():
    subject = 'Bulk Create Notification'
    message = 'Employees have been created successfully through bulk create.'
    recipients_list = [settings.EMAIL_HOST_USER]  # Replace with your email address or a list of recipients

    # Create a separate thread to send the email asynchronously
    email_thread = Thread(target=send_mail, args=(subject, message, settings.EMAIL_HOST_USER, recipients_list))
    email_thread.start()


def send_email_async(subject, message, recipient_list):
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list,  html_message=message)

def send_login_email_async(user):
    subject = 'Login Notification'
    message = f'Hi {user.username}, you have successfully logged in.'
    email_from = settings.EMAIL_HOST_USER
    recipients_list = [user.email]

    try:
        send_mail(subject, message, email_from, recipients_list)
    except Exception as e:
        print(str(e))


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee.csv" '
    
    writer=csv.writer(response)
    writer.writerow( ["eid ", "ename", "eemail"," ephone", "eage"])
    employees = Employee.objects.all()
    
    for employee in employees:
        writer.writerow([employee.eid, employee.ename, employee.eemail,employee.ephone,employee.eage])
    return response   
 
def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="employee.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Employee"

    # Add headers
    headers = ["eid ", "ename", "eemail"," ephone", "eage"]
    ws.append(headers)

    # Add data from the model
    employees = Employee.objects.all()
    for employee in employees:
        ws.append([employee.eid, employee.ename, employee.eemail,employee.ephone,employee.eage])

  
    wb.save(response)
    return response 



def get_success_url(self):
    
    return redirect("/home")
    

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return render(request, 'login.html', {'error_message': 'Username and password are required.'})
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
       
            
            return redirect('employee:landing')
    return render(request, 'login.html')

def user_logout(request):
    
       logout(request)
       messages.info(request, "You have successfully logged out.") 
       return render(request, 'login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email=request.POST.get('email')
        # form = UserCreationForm(data = request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     username = form.cleaned_data.get('username')
        user=User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        # subject = 'Welcome to employee registration'
        # message= f'Hi {user.username}, thank you for registering'
        # print(message)
        # email_from = settings.EMAIL_HOST_USER
        # print(subject, email_from)
        # recipients_list = [user.username,]
        # print(recipients_list)
        # try:
        #     x=send_mail(subject,message,email_from,recipients_list)
        # except Exception as e:
        #     print(str (e))
        # subject = 'Welcome to employee registration'
        # message = render_to_string('email_sent.html', {'user': user})
        # plain_message = strip_tags(message)
        # recipients_list = [user.email]

        # # Create a separate thread to send the email asynchronously
        # email_thread = Thread(target=send_email_async, args=(subject, plain_message, recipients_list))
        # email_thread.start()
        subject = 'Welcome to employee registration'
        message = render_to_string('email_sent.html', {'user': user})
        plain_message = strip_tags(message)
        recipients_list = [user.username]

        # Create a separate thread to send the email asynchronously
        email_thread = Thread(target=send_email_async, args=(subject, plain_message, recipients_list))
        email_thread.start()

        # return redirect('employee:user_login')

    # return render(request, 'register.html')  
        return redirect('employee:user_login')
            # messages.success(request, f'Account created for {username}!')
        # return redirect('employee:user_login')
    # else:
    #     messages.error(request, 'Error in registration. Please check the form.')
    # form = UserCreationForm()
    return render(request, 'register.html')

    

def emp(request):
    if request.method == "POST":
        form = EmployeeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            eemail = form.cleaned_data['eemail']

            existing_employee = Employee.objects.filter(eemail=eemail).first()

            if existing_employee:
                form.add_error('eemail', 'An employee with this email already exists. You can edit the existing record.')
            else:
                form.save()
                return redirect("employee:landing")
            
    form = EmployeeForm()
    return render(request, 'index.html', {'form': form})



# def home(request):  
#     employees = Employee.objects.all()  
#     paginator = Paginator(employees, 6)
#     page = request.GET.get('page')
#     try:
#         employee_page = paginator.page(page)
#     except PageNotAnInteger:
#         # If the page is not an integer, deliver the first page
#         employee_page = paginator.page(1)
#     except EmptyPage:
#         # If the page is out of range, deliver the last page
#         employee_page = paginator.page(paginator.num_pages)

#     return render(request, "home.html", {'employee_page': employee_page})

def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})  

def update(request, id):
    employee = Employee.objects.get(id=id)

    if request.method == "POST":
        form = EmployeeForm(request.POST,request.FILES, instance=employee)

        if form.is_valid():
          
            if 'eemail' in form.changed_data:
                 
                 try:
                     form.validate_unique()
                 except forms.ValidationError as e:
                   
                    form.add_error('eemail', str(e))
                    return render(request, 'edit.html', {'employee': employee, 'form': form})

            # Save the form if it's valid or email field hasn't changed
            form.save()
            return redirect("employee:landing")
    form = EmployeeForm(instance=employee)
    return render(request, 'edit.html', {'employee': employee, 'form': form})

def destroy(request, id):  
    employee = Employee.objects.get(id=id)  
    employee.delete()  
    return redirect("employee:landing") 




def landing(request):
    if not request.user.is_authenticated:
        return redirect('employee:user_login')
    employees = Employee.objects.all()
    print(employees.count())
    paginator = Paginator(employees, per_page=10)
    page = request.GET.get('page')
    try:
        employee_page = paginator.page(page)
    except PageNotAnInteger:
        employee_page = paginator.page(1)
    except EmptyPage:
        employee_page = paginator.page(paginator.num_pages)
    context = {
        "employees": employee_page
    }
    return render(request, 'home.html', context)