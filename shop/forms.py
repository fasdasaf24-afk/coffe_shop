from django import forms
from .models import Order, SupportMessage, Review

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address']

class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['name', 'message']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'text', 'rating']
