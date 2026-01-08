from django.urls import path
from . import views
urlpatterns = [
    path('',views.login_choice, name='login_choice'),
    path('management_login/',views.management_login, name='management_login'),
    path('staff_login/',views.staff_login, name='staff_login'),
    path('management_dashboard/',views.management_dashboard, name='management_dashboard'),
    path('create-staff/', views.add_staff, name='add_staff'),
    path('staff/<int:staff_id>/bills<str:period>/', views.view_staff_bill, name='view_staff_bills'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/add-bill/', views.add_bill, name='add_bill'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/bills/<str:period>/', views.staff_view_bills, name='staff_bills'),

]