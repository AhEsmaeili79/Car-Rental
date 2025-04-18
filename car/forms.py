from django import forms
from .models import Car, Review

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'image', 'image2', 'image3', 'image4', 'image5', 'city', 'capacity', 'price_per_day', 'with_driver']
        
        # Custom widgets to apply styles
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'مدل خودرو'}),
            'image': forms.ClearableFileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
            'image3': forms.ClearableFileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
            'image4': forms.ClearableFileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
            'image5': forms.ClearableFileInput(attrs={'class': 'input-field', 'accept': 'image/*'}),
            'city': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'شهر'}),
            'capacity': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'ظرفیت'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'قیمت هر روز'}),
            'with_driver ': forms.CheckboxInput(attrs={'class': 'input-checkbox'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input-field'  

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
