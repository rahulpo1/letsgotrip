from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, TourPackage, Booking

#  User Registration
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ''

#  Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'})
    )

#  Vendor Tour Package Form
class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ['title', 'description', 'price', 'duration', 'image', 'category', 'expiry_date']

# Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_people', 'phone', 'email']
        labels = {
            'number_of_people': 'Number of People',
            'phone': 'Phone Number',
            'email': 'Email Address',
        }
