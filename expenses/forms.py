from django import forms
from expenses.models import ExpenseModel

class UserForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white  ','placeholder':'enter username','style': 'color: white;'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control bg-dark text-white ','placeholder':'enter your email'}))
    password=forms.CharField(max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control bg-dark text-white ','placeholder':'enter password'}))
    
    
class LoginForm(forms.Form):
    
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control bg-dark text-white ','placeholder':'enter username'}))
    password=forms.CharField(max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control bg-dark text-white ','placeholder':'enter password'}))


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseModel
        fields = ['name', 'amount', 'category', 'date', 'description']
        labels = {
            'name': 'Transaction Name',
            'amount': 'Amount',
            'category': 'Transaction Type',
            'description': 'Additional Details',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white '}),
            'amount': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white'}),
            'category': forms.Select(attrs={'class': ' form-select bg-dark text-white'  }),
            'date': forms.DateInput(attrs={'class': 'form-control bg-dark text-white','type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 4, 'cols': 20}),
        }

class FeedbackForm(forms.Form):
    name = forms.CharField( max_length=100,widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-white', }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-white', }))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 4, }))


