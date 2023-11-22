from django import forms
from django.forms.widgets import DateInput
from .models import Stock

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['doses','med_name','quantity','mrp','batch_no','expiry_date']
        widgets = {
            'expiry_date': DateInput(attrs={'type': 'date', 'class': 'custom-date-input'}),
        }
