# from django import forms  
# from employee.models import Employee 
# class EmployeeForm(forms.ModelForm):  
#     class Meta:  
#         model = Employee  
#         fields = "__all__"  
        
#     def validate_eemail(self):
#         eemail = self.cleaned_data.get('eemail')
#         if Employee.objects.filter(eemail=eemail).exists():
#             raise forms.ValidationError('This email address is already in use. Please provide a different email.')
#         return eemail    


from django import forms

from employee.models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

 