# house/templatetags/arabic_numerals.py
from django import template

register = template.Library()

@register.filter
def arabic_numerals(value):
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_to_arabic = str.maketrans("0123456789", arabic_digits)
    return str(value).translate(english_to_arabic)
