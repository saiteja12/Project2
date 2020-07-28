from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.views.generic import TemplateView, ListView
from da.models import *
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models import Count
from rest_framework import serializers
from django.db.models.functions import TruncMonth
from django.conf import settings
from . import notifier

# Create your views here.
from . import forms

class LoginPageView(TemplateView):
    template_name = "login.html"

@csrf_exempt
def loginVerify(request):
    if request.method == "POST":
        login = Login.objects.filter(
        username = json.loads(request.body)['username'],
        password = json.loads(request.body)['password']
        )
        if login:
            request.session['username'] = json.loads(request.body)['username']
            request.session['password'] = json.loads(request.body)['password']
            return HttpResponse(json.dumps({'success':True}))
        else:
            return HttpResponse(json.dumps({'success':False}))

def login_check(function):
    def wrap(request, *args, **kwargs):
        session = request.session # this is a dictionary with session keys
        print(session)
        if session.get('username') and session.get('password'):
            # the decorator is passed and you can handle the request from the view
            return function(request, *args, **kwargs)
        else:
            return redirect('LoginPage')
    return wrap

def logout(request):
    if request.method=='GET':
        request.session.flush()
        return HttpResponse(json.dumps({'success':True}))

@login_check
def HomePageView(request):
    context={}
    return render(request,'index.html',context)
# class HomePageView(TemplateView):
#     template_name = "index.html"


@login_check
def ticket_form(request):
    form = forms.RaiseTicketForm()
    if request.method == "POST":
        form = forms.RaiseTicketForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                Subject="Your request has been submitted."
                cc=["boyapatisaiteja@gmail.com"]
                From="boyapatisaiteja@gmail.com"
                template='D:\\Django Python\\tickets\\da\\templates\\email.html'
                to = [form.cleaned_data['email_address']]
                firstname=form.cleaned_data['requestor_name']
                email='id'
                with open(template,'r') as fh:
                    sub_content=fh.read()
                sub_content=sub_content.replace('#FirstName',firstname).replace('#user_email',email)
                notifier.emailNotify(From, to, cc, Subject, sub_content)
                return redirect('TicketList')
            except Exception as e:
                print(str(e))
                print('email not sent')
                return redirect('TicketList')
    context = {'form':form}
    return render(request,'form.html',context)
@login_check
def ticket_list(request):
    context={'ticket_list':RaiseTicket.objects.all().order_by('-request_date')}
    return render(request,'ticket_list.html',context)
@login_check
def dashboard(request):
    data1=RaiseTicket.objects.values('request_date__month').annotate(total=Count('request_date__month')) 
    data2= RaiseTicket.objects.values('request_type').annotate(Count('request_type'))
    data3= RaiseTicket.objects.values('account_name').annotate(Count('account_name'))
    data4=RaiseTicket.objects.values('assignee').annotate(Count('assignee'))


    monthly_list=[]
    no_of_tickets_monthly=[]
    month_labels=[]
    

    for data in data1:
        monthly_data={}
        monthly_data['month']=str(data['request_date__month'])
        monthly_data['total']=data['total']
        monthly_list.append(monthly_data)
    
    for i in range(len(monthly_list)):
        month_labels.append(monthly_list[i]['month'])
        no_of_tickets_monthly.append(monthly_list[i]['total'])


    labels=[]
    no_of_ticket_types=[]
    request_list=[]

    for data in data2:
        requests_data={}
        requests_data['request_type']=data['request_type']
        requests_data['request_count']=data['request_type__count']
        request_list.append(requests_data)
    
    for i in range(len(request_list)):
        labels.append(request_list[i]['request_type'])
        no_of_ticket_types.append(request_list[i]['request_count'])

    no_of_accounts=[]
    accounts_list=[]
    account_labels=[]

    for data in data3:
        accounts_data={}
        accounts_data['account_name']=data['account_name']
        accounts_data['account_count']=data['account_name__count']
        accounts_list.append(accounts_data)
    
    for i in range(len(accounts_list)):
        account_labels.append(accounts_list[i]['account_name'])
        no_of_accounts.append(accounts_list[i]['account_count'])
        

    no_of_projects_by_each_assignee=[]
    assignees_list=[]
    assignee_labels=[]

    for data in data4:
        assignee_data={}
        assignee_data['assignee_name']=data['assignee']
        assignee_data['project_count']=data['assignee__count']
        assignees_list.append(assignee_data)
    
    for i in range(len(assignees_list)):
        assignee_labels.append(assignees_list[i]['assignee_name'])
        no_of_projects_by_each_assignee.append(assignees_list[i]['project_count'])

    context={
            'month_labels':month_labels,
            'no_of_tickets_monthly':no_of_tickets_monthly,
            'labels':labels,
            'no_of_ticket_types':no_of_ticket_types,
            'account_labels':account_labels,
            'no_of_accounts':no_of_accounts,
            'assignee_labels':assignee_labels,
            'no_of_projects_by_each_assignee':no_of_projects_by_each_assignee
        }

    return render(request,'dashboard.html',context)

@login_check
def dash(request):
    # labels1=['a','b','c','d']
    # data1=[10,20,3,34]
    # data1= [RaiseTicket.objects.all().count()]
    data1=RaiseTicket.objects.values('request_date__month').annotate(total=Count('request_date__month')) 
    data2= RaiseTicket.objects.values('request_type').annotate(Count('request_type'))
    data3= RaiseTicket.objects.values('account_name').annotate(Count('account_name'))
    data4=RaiseTicket.objects.values('assignee').annotate(Count('assignee'))


    monthly_list=[]
    no_of_tickets_monthly=[]
    month_labels=[]
    

    for data in data1:
        monthly_data={}
        monthly_data['month']=str(data['request_date__month'])
        monthly_data['total']=data['total']
        monthly_list.append(monthly_data)
    
    for i in range(len(monthly_list)):
        month_labels.append(monthly_list[i]['month'])
        no_of_tickets_monthly.append(monthly_list[i]['total'])


    labels=[]
    no_of_ticket_types=[]
    request_list=[]

    for data in data2:
        requests_data={}
        requests_data['request_type']=data['request_type']
        requests_data['request_count']=data['request_type__count']
        request_list.append(requests_data)
    
    for i in range(len(request_list)):
        labels.append(request_list[i]['request_type'])
        no_of_ticket_types.append(request_list[i]['request_count'])

    no_of_accounts=[]
    accounts_list=[]
    account_labels=[]

    for data in data3:
        accounts_data={}
        accounts_data['account_name']=data['account_name']
        accounts_data['account_count']=data['account_name__count']
        accounts_list.append(accounts_data)
    
    for i in range(len(accounts_list)):
        account_labels.append(accounts_list[i]['account_name'])
        no_of_accounts.append(accounts_list[i]['account_count'])
        

    no_of_projects_by_each_assignee=[]
    assignees_list=[]
    assignee_labels=[]

    for data in data4:
        assignee_data={}
        assignee_data['assignee_name']=data['assignee']
        assignee_data['project_count']=data['assignee__count']
        assignees_list.append(assignee_data)
    
    for i in range(len(assignees_list)):
        assignee_labels.append(assignees_list[i]['assignee_name'])
        no_of_projects_by_each_assignee.append(assignees_list[i]['project_count'])

    data={
        'month_labels':month_labels,
        'no_of_tickets_monthly':no_of_tickets_monthly,
        'labels':labels,
        'no_of_ticket_types':no_of_ticket_types,
        'account_labels':account_labels,
        'no_of_accounts':no_of_accounts,
        'assignee_labels':assignee_labels,
        'no_of_projects_by_each_assignee':no_of_projects_by_each_assignee
    }

    return JsonResponse(data)

