from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import *



PAYMENT_CHOICES = (
    
    
    ('S','CashOnDelevery'),
)


class CheckoutForm(forms.Form):
    fname = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
        'placeholder':'first-name',
        'class':'form-control'
    }))
    lname = forms.CharField(max_length=200,widget=forms.TextInput(attrs={
        'placeholder':'last-name',
        'class':'form-control'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder':'email-address',
        'class':'form-control'
    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'mobile-number',
        'class':'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'address',
        'class':'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select'
        })
    )
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'City',
        'class':'form-control'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'State',
        'class':'form-control'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Zipcode',
        'class':'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'id': 'billing'
    }))

    different_billing_address = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'id': 'shipto'
    }))

    save_info = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input',
        'id': 'save'
    }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices= PAYMENT_CHOICES)


class BillingIt(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['fname','lname','email','mobile','address','country','city','state','zipcode','payment_option']



class ProductReview(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['name','email','comment']