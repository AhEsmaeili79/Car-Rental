from django import forms
from .models import Car, Review

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'image', 'image2', 'image3', 'image4', 'image5', 'city', 'capacity', 'price_per_day', 'with_driver']
        
        labels = {
            'name': 'مدل و برند خودرو',
            'image': 'تصویر اصلی خودرو',
            'image2': 'تصویر اضافی ۱',
            'image3': 'تصویر اضافی ۲',
            'image4': 'تصویر اضافی ۳',
            'image5': 'تصویر اضافی ۴',
            'city': 'شهر',
            'capacity': 'ظرفیت مسافر',
            'price_per_day': 'قیمت روزانه',
            'with_driver': 'با راننده'
        }
        
        help_texts = {
            'name': 'نام کامل مدل و برند خودرو را وارد کنید',
            'image': 'تصویر اصلی خودرو را آپلود کنید (اجباری)',
            'image2': 'تصویر اضافی خودرو را آپلود کنید (اختیاری)',
            'image3': 'تصویر اضافی خودرو را آپلود کنید (اختیاری)',
            'image4': 'تصویر اضافی خودرو را آپلود کنید (اختیاری)',
            'image5': 'تصویر اضافی خودرو را آپلود کنید (اختیاری)',
            'city': 'شهر محل خودرو را وارد کنید',
            'capacity': 'حداکثر تعداد مسافر را وارد کنید',
            'price_per_day': 'قیمت اجاره روزانه را به تومان وارد کنید',
            'with_driver': 'در صورت ارائه خدمات راننده این گزینه را انتخاب کنید'
        }
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'e.g., Toyota Camry 2023'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'input-field',
                'accept': 'image/*',
                'required': True
            }),
            'image2': forms.ClearableFileInput(attrs={
                'class': 'input-field',
                'accept': 'image/*'
            }),
            'image3': forms.ClearableFileInput(attrs={
                'class': 'input-field',
                'accept': 'image/*'
            }),
            'image4': forms.ClearableFileInput(attrs={
                'class': 'input-field',
                'accept': 'image/*'
            }),
            'image5': forms.ClearableFileInput(attrs={
                'class': 'input-field',
                'accept': 'image/*'
            }),
            'city': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'e.g., Tehran'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'input-field',
                'min': '1',
                'max': '10',
                'placeholder': 'e.g., 4'
            }),
            'price_per_day': forms.NumberInput(attrs={
                'class': 'input-field',
                'min': '0',
                'placeholder': 'e.g., 500000'
            }),
            'with_driver': forms.CheckboxInput(attrs={
                'class': 'input-checkbox'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input-field'
            
    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity < 1:
            raise forms.ValidationError("Capacity must be at least 1")
        if capacity > 10:
            raise forms.ValidationError("Capacity cannot be more than 10")
        return capacity
        
    def clean_price_per_day(self):
        price = self.cleaned_data.get('price_per_day')
        if price < 0:
            raise forms.ValidationError("Price cannot be negative")
        return price

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
