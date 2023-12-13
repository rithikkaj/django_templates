from django.db import models


# Create your models here.
class Employee(models.Model):  
    eid = models.CharField(max_length=20)  
    ename = models.CharField(max_length=100)  
    eemail = models.EmailField(unique=True)  
    ephone = models.CharField(max_length=12)
    eage = models.IntegerField(null=True, default=None)  
    eimage = models.ImageField(null=True,blank=True)
    
    class Meta:  
        db_table = "employee"  
    def __str__(self):
        return self.eemail
    
    