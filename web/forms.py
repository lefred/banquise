from django import forms
from django.contrib.admin import widgets  
from banquise.web.models import Customer, Host, Package, ServerPackages, Contract

class ContractForm(forms.ModelForm):
    start_date = forms.DateField(('%Y-%m-%d',),   
        widget=forms.DateTimeInput(format='%Y-%m-%d', attrs={
            'class':'input',
            'readonly':'readonly',
            'size':'10'
        })
    )
    end_date = forms.DateField(('%Y-%m-%d',),   
        widget=forms.DateTimeInput(format='%Y-%m-%d', attrs={
            'class':'input',
            'readonly':'readonly',
            'size':'10'
        })
    )
    class Meta:
        model = Contract
        fields = ('start_date','end_date')

class PackageForm(forms.ModelForm):
    name = forms.CharField(required=False)
    arch = forms.CharField(required=False)
    version = forms.CharField(required=False)
    release = forms.CharField(required=False)
    class Meta:
        model = Package
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        