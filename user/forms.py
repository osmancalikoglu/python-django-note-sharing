from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
        }


CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Izmir', 'Izmir')
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'school', 'image']
        widgets = {
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address': TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city': Select(attrs={'class': 'form-control', 'placeholder': 'City'}, choices=CITY),
            'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'school': TextInput(attrs={'class': 'form-control', 'placeholder': 'School'}),
            'image': FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'})
        }

