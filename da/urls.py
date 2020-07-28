from django.urls import path
from da import views
from da import forms

urlpatterns = [
    path('',views.LoginPageView.as_view(),name='LoginPage'),
    path('login/',views.loginVerify,name='login verify'),
    path('logout/',views.logout,name='logout'),
    path('home/',views.HomePageView,name='HomePage'),
    path('raiseticket/',views.ticket_form,name='FormsPage'),
    path('list/',views.ticket_list,name='TicketList'),
    path('Dashboard/',views.dashboard,name='Dashboard'),
    path('test/',views.dash,name='dash'),
]
