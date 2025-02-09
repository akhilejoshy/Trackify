"""
URL configuration for ExpenseTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from expenses import views

urlpatterns = [
    path('register/',views.Registerview.as_view(), name='register'),
    path('',views.Login.as_view(),name='login'),
    path('home/',views.Home.as_view(),name='home'),
    path('add_expense/', views.AddExpense.as_view(), name='addexpense'),
    path('expenses/',views.ExpenseList.as_view(),name='expenses'),
    path('settings/',views.Settings.as_view(),name='settings'),
    path('support/',views.Support.as_view(),name='support'),
    path('logout/',views.Logout.as_view(),name='logout'),
    path('delete/<int:id>/',views.DeleteExpense.as_view(),name='delete'),
    path('update/<int:id>/',views.UpdateExpense.as_view(),name='update'),
    path('expense/<int:pk>/', views.ExpenseDetail.as_view(), name='expense_detail'),
    path('feedback/',views.Feedback.as_view(), name='feedback'),




]
