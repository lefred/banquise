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
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if start_date < end_date:
            return end_date
        raise forms.ValidationError(u'end date %s is before start date' % end_date )

    class Meta:
        model = Contract
        fields = ('start_date','end_date')
    
    
class PackageForm(forms.ModelForm):
    name = forms.CharField(required=False)
    arch = forms.CharField(required=False)
    version = forms.CharField(required=False)
    release = forms.CharField(required=False)
    repo = forms.CharField(required=False)
    class Meta:
        model = Package
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        