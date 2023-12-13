from django.urls import path
from .views import *
from django.urls import path
from .views import export_to_excel


app_name = "employee"

urlpatterns = [
    path('',landing, name='landing'),
    path('login/', user_login, name='user_login'),  
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),
    path('emp/',emp, name = "emp"),
    # path('employee/',employee_show, name = "employee_show"),
    path('emp/update',emp),
    path('employee/<int:id>/edit',update),
    path('employee/<int:id>/delete', destroy),
     path('export/', export_to_excel, name='export_to_excel'),
    path('exports/',export_csv, name='export_csv'),
    path('bulk_create_from_data/', bulk_create_from_data, name='bulk_create_from_data')
]