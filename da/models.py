from django.db import models
from django.utils import timezone
# Create your models here.

class RaiseTicket(models.Model):
    x=[('P1','Priority_1'),('P2','Priority_2'),('P3','Priority_3'),('P4','Priority_4')]
    tkt_sts=[('new','new'),('open','open'),('development','development'),('testing','testing'),
    ('closed','closed')]
    requestor_name = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=50)
    account_name =  models.CharField(max_length=30)
    approver_name = models.CharField(max_length=30)
    request_type = models.CharField(max_length=30)
    requestor_priority = models.CharField(max_length=2,choices=x,default='P1')
    task_status = models.CharField(max_length=50,choices=tkt_sts,default='new')
    request_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    assignee = models.CharField(max_length = 50,default='null')
    request_description = models.TextField()
    def __int__(self):
        return self.id


class Login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=15)
    role = models.CharField(max_length=10)
    def __str__(self):
        return self.username
