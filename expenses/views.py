from django.shortcuts import render,redirect
from django.views import View
from expenses.forms import UserForm,LoginForm,ExpenseForm,FeedbackForm
from expenses.models import User,ExpenseModel
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Case, When, DecimalField, F, ExpressionWrapper
from django.db.models.functions import TruncMonth
import datetime
import json



# Create your views here.

class Registerview(View):
    def get(self,request):
        form= UserForm() 
        return render(request,'authentication/register.html',{'form':form})
    
    def post(self,request):
        form= UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            # return render(request,'register.html',{'form':form})
            return redirect('login')
        return render(request,'authentication/register.html',{'form':form})

class Login(View):
    def get(self, request):
        form = LoginForm()  
        return render(request,'authentication/login.html',{'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            pswd = form.cleaned_data.get('password')
            user = authenticate(request, username=user_name, password=pswd)
            if user:
                login(request, user)
                return redirect('home')
            else:
                message = 'Invalid username or password'  
                return render(request, 'authentication/login.html', {'form': form, 'message': message})
        return render(request, 'authentication/login.html', {'form': form})

        

class Home(View):
    def get(self, request):
        # Get today's date
        today = datetime.date.today()
        default_date = f"{today.year}-{today.month:02d}"  # Format YYYY-MM

        # Get the selected date from the GET request or set default to current month
        date_filter = request.GET.get('date', default_date)

        # Extract year and month from the selected date
        filter_year, filter_month = map(int, date_filter.split('-'))

        # Filter expenses for the selected month (or default month)
        data = ExpenseModel.objects.filter(user=request.user, date__year=filter_year, date__month=filter_month)

        # Calculate total credit and total debit for the selected month
        total_credit = data.filter(category='credit').aggregate(total=Sum('amount'))['total'] or 0
        total_debit = data.filter(category='debit').aggregate(total=Sum('amount'))['total'] or 0

        # Calculate balance
        balance = total_credit - total_debit

        # Get summary for the graph (remains unchanged)
        summary = (
            ExpenseModel.objects.filter(user=request.user)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(
                total_credit=Sum(
                    Case(When(category='credit', then='amount'), default=0, output_field=DecimalField())
                ),
                total_debit=Sum(
                    Case(When(category='debit', then='amount'), default=0, output_field=DecimalField())
                ),
            )
            .annotate(
                total=F('total_credit') + F('total_debit')  # Fix: Use F() expressions
            )
            .annotate(
                credit_percentage=ExpressionWrapper(
                    (F('total_credit') * 100) / (F('total_credit') + F('total_debit')),
                    output_field=DecimalField()
                ),
                debit_percentage=ExpressionWrapper(
                    (F('total_debit') * 100) / (F('total_credit') + F('total_debit')),
                    output_field=DecimalField()
                ),
            )
            .order_by('month')
        )

        # Prepare data for the graph
        summary_data = [
            {
                'month': str(item['month'].strftime('%Y-%m')),
                'credit_percentage': float(item['credit_percentage']),
                'debit_percentage': float(item['debit_percentage']),
                'total_expens': float(item['total']),  
             
            }
            for item in summary
        ]


        return render(request, 'expenses/home.html', {
        'summary_data': json.dumps(summary_data),  # Convert list to JSON
            'total_credit': total_credit,  # Total credit for the selected/default month
            'total_debit': total_debit,  # Total debit for the selected/default month
            'balance': balance,  # Balance calculation
            'selected_date': date_filter,  # Ensures the input field keeps the selected/default date
        })


    


class AddExpense(View):
    def get(self, request):
        form = ExpenseForm()
        data=ExpenseModel.objects.all()

        return render(request, 'expenses/addexpense.html', {'form': form,'data':data})
    
    
    def post(self, request):
        if not request.user.is_authenticated:  
            return redirect('login')  
        form = ExpenseForm(request.POST)
        if form.is_valid():
            ExpenseModel.objects.create(**form.cleaned_data,user=request.user)
        form = ExpenseForm()
        return render(request, 'expenses/addexpense.html', {'form': form})



class ExpenseList(View):
    def get(self, request):
        if not request.user.is_authenticated:  
            return redirect('login')  

        data = ExpenseModel.objects.filter(user=request.user)

        category = request.GET.get('category', '')
        date_filter = request.GET.get('date', '')

        if category:
            data = data.filter(category=category)

        if date_filter:
            year, month = date_filter.split('-')
            data = data.filter(date__year=year, date__month=month)

        return render(request, 'expenses/expenses.html', {'data': data})




class ExpenseDetail(View):
    def get(self,request,pk):
        data=ExpenseModel.objects.get(id=pk)
        return render(request,'expenses/detail.html',{'data':data})    

class DeleteExpense(View):
    def get(self,request,id):
        ExpenseModel.objects.get(id=id).delete()
        return redirect('expenses')
    

class UpdateExpense(View):
    def get(self,request,id):
        data=ExpenseModel.objects.get(id=id)
        form=ExpenseForm(instance=data)
        return render(request,'expenses/update.html',{'form':form})
        
    def post(self,request,id):
        data=ExpenseModel.objects.get(id=id)
        form=ExpenseForm(request.POST,instance=data)
        form.save()
        return redirect('expenses')
    
class Settings(View):
    def get(self,request):

        return render(request,'expenses/settings.html')
    
class Support(View):
    def get(self,request):
        return render(request,'expenses/support.html')
    
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('login')
    
# class Profile(View):
#     def get(self,request):
#         user_id=request.user.id
#         user=User.objects.get(id=user_id)
#         return render(request,'expenses/profile.html',{'user':user})
class Feedback(View):
    def get(self, request):
        form = FeedbackForm()
        return render(request, 'expenses/feedback/feedback.html', {'form': form})
    def post(self,request):
        return render(request,'expenses/feedback/message.html')
