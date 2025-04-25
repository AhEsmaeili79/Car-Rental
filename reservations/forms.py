from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Order
from django.utils import timezone

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_date', 'return_date', 'number_of_passengers']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'number_of_passengers': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
        }

    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get('pickup_date')
        return_date = cleaned_data.get('return_date')
        number_of_passengers = cleaned_data.get('number_of_passengers')

        if pickup_date and return_date:
            if return_date <= pickup_date:
                raise forms.ValidationError('Return date must be after pickup date.')
            
            if pickup_date < timezone.now().date():
                raise forms.ValidationError('Pickup date cannot be in the past.')

        if number_of_passengers is not None and number_of_passengers < 1:
            raise forms.ValidationError('Number of passengers must be at least 1.')

