from django.db import models

# Create your models here.

class Staff(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=25)
    role = models.CharField(max_length=20, default="Staff")

    def __str__(self):
        return self.username
    
class Bill(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    cust_name = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.cust_name} - {self.staff.username} - {self.date}"