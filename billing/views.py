from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Staff , Bill
from datetime import date, timedelta

# Create your views here.
def login_choice(req):
    return render(req, 'billing/login_choice.html')

def staff_login(req):
    return render(req, 'billing/staff_login.html')


def management_login(req):
  
    admin_name = "Admin"
    admin_pwd = "Admin@123"

    if req.method == "POST":
        uname = req.POST.get('uname')
        pwd = req.POST.get('pwd')

        if uname == admin_name and pwd == admin_pwd:
            
            return render(req, 'billing/management_dashboard.html')
        else:
            messages.error(req, "Invalid Username or Password")

    return render(req, 'billing/management_login.html')



def management_dashboard(req):
   
    return render(req, 'billing/management_dashboard.html')

def add_staff(req):
    if req.method == "POST":
        uname = req.POST.get('uname')
        pwd = req.POST.get('pwd')

        if Staff.objects.filter(username=uname).exists():
            messages.error(req, "User name already exsist")

        else:
            Staff.objects.create(username=uname, password=pwd)
            messages.error(req, "Staff added successfully")

    staff_list = Staff.objects.all()
    return render(req, 'billing/add_staff.html',{'staff_list' : staff_list})



def view_staff_bill(req , staff_id, period):   
    staff = Staff.objects.get(id=staff_id)

    today = date.today()

    if period == 'daily':
        bills = Bill.objects.filter(staff=staff, date=today)
    elif period == 'weekly':
        week_ago = today - timedelta(days=7)
        bills = Bill.objects.filter(staff=staff, date__gte=week_ago)
    elif period == 'monthly':
        month_ago = today - timedelta(days=30)
        bills = Bill.objects.filter(staff=staff, date__gte=month_ago)
    else:
        bills = Bill.objects.filter(staff=staff)

    return render(req, 'billing/view_staff_bills.html', {'staff': staff, 'bills': bills, 'period': period})

def staff_login(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        try:
            staff = Staff.objects.get(username=uname, password=pwd)
           
            request.session['staff_id'] = staff.id
            return redirect('staff_dashboard')
        except Staff.DoesNotExist:
            messages.error(request, "Invalid username or password")

    return render(request, 'billing/staff_login.html')

def staff_dashboard(request):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('staff_login')

    staff = Staff.objects.get(id=staff_id)
    return render(request, 'billing/staff_dashboard.html', {'staff': staff})


def add_bill(request):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('staff_login')

    staff = Staff.objects.get(id=staff_id)

    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        service_type = request.POST.get('service_type')
        amount = request.POST.get('amount')

        Bill.objects.create(
            staff=staff,
            cust_name=customer_name,
            service_type=service_type,
            amount=amount
        )
        messages.success(request, "Bill added successfully!")

    return render(request, 'billing/add_bill.html')

def staff_logout(request):
    request.session.flush()  
    return redirect('staff_login')

def staff_view_bills(request, period):
    staff_id = request.session.get('staff_id')
    if not staff_id:
        return redirect('staff_login')

    staff = Staff.objects.get(id=staff_id)
    today = date.today()

    if period == "daily":
        bills = Bill.objects.filter(staff=staff, date=today)

    elif period == "weekly":
        bills = Bill.objects.filter(
            staff=staff,
            date__gte=today - timedelta(days=7)
        )

    elif period == "monthly":
        bills = Bill.objects.filter(
            staff=staff,
            date__gte=today - timedelta(days=30)
        )

    else:
        bills = Bill.objects.filter(staff=staff)

    return render(request, 'billing/staff_bills.html', {
        'bills': bills,
        'period': period
    })