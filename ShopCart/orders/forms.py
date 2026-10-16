from django import forms
from django.core.validators import RegexValidator
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100,label='Full name')
    email = forms.EmailField()
    phone = forms.CharField(max_length=10,validators=[RegexValidator(r'^[6-9][0-9]{9}$','Enter a valid 10-digit Indian mobile number.')])
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3}),max_length=500,label='Street address')
    city = forms.CharField(max_length=80)
    postcode = forms.CharField(max_length=6,label='PIN code',validators=[RegexValidator(r'^[1-9][0-9]{5}$','Enter a valid 6-digit PIN code.')])
    checkout_token = forms.UUIDField(widget=forms.HiddenInput)
