from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Order
from django.utils import timezone
from datetime import datetime, date
import logging
from persiantools.jdatetime import JalaliDate

logger = logging.getLogger(__name__)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['pickup_date', 'return_date', 'number_of_passengers']
        widgets = {
            'pickup_date': forms.DateInput(attrs={
                'class': 'form-control',
                'data-jdp': '',
                'data-jdp-min-date': 'today',
                'data-jdp-only-date': '',
                'autocomplete': 'off'
            }),
            'return_date': forms.DateInput(attrs={
                'class': 'form-control',
                'data-jdp': '',
                'data-jdp-min-date': 'today',
                'data-jdp-only-date': '',
                'autocomplete': 'off'
            }),
            'number_of_passengers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'فقط عدد',
                'autocomplete': 'off'
            })
        }

    def parse_jalali_date(self, date_str):
        try:
            if not date_str:
                return None
            # Handle both YYYY/MM/DD and YYYY-MM-DD formats
            if '-' in date_str:
                year, month, day = map(int, date_str.split('-'))
            else:
                year, month, day = map(int, date_str.split('/'))
            
            logger.info(f"Parsed date components - year: {year}, month: {month}, day: {day}")
            jalali_date = JalaliDate(year, month, day)
            gregorian_date = jalali_date.to_gregorian()
            logger.info(f"Converted to Gregorian: {gregorian_date}")
            return gregorian_date
        except (ValueError, TypeError, AttributeError) as e:
            logger.error(f"Error parsing Jalali date {date_str}: {e}")
            return None

    def clean(self):
        cleaned_data = super().clean()
        pickup_date_str = self.data.get('pickup_date')
        return_date_str = self.data.get('return_date')
        
        logger.info(f"Raw form data - pickup_date: {pickup_date_str} (type: {type(pickup_date_str)})")
        logger.info(f"Raw form data - return_date: {return_date_str} (type: {type(return_date_str)})")
        
        # Convert Jalali dates to Gregorian
        pickup_date = self.parse_jalali_date(pickup_date_str)
        if not pickup_date:
            raise forms.ValidationError('تاریخ تحویل نامعتبر است.')
        cleaned_data['pickup_date'] = pickup_date
        
        return_date = self.parse_jalali_date(return_date_str)
        if not return_date:
            raise forms.ValidationError('تاریخ بازگشت نامعتبر است.')
        cleaned_data['return_date'] = return_date
        
        number_of_passengers = cleaned_data.get('number_of_passengers')

        if pickup_date and return_date:
            today = date.today()
            logger.info(f"Date comparison - pickup: {pickup_date}, return: {return_date}, today: {today}")
            
            if return_date <= pickup_date:
                raise forms.ValidationError('تاریخ برگشت باید بعد از تاریخ تحویل باشد.')
            
            if pickup_date < today:
                raise forms.ValidationError('تاریخ تحویل نمی‌تواند در گذشته باشد.')

        if number_of_passengers is not None and number_of_passengers < 1:
            raise forms.ValidationError('تعداد مسافران باید حداقل 1 نفر باشد.')
        
        return cleaned_data

