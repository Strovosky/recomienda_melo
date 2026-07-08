from django.forms import EmailField, ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile


class UserRegistrationForm(UserCreationForm):
    "This is like UserCreationForm but we can add an email."
    email = EmailField(max_length=100, min_length=7, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(ModelForm):
    """This form will update the user's email"""
    email = EmailField(max_length=100, min_length=7, required=False)
    
    class Meta:
        model = User
        fields = ["email"]


class ProfileUpdateForm(ModelForm):
    """This form will update the user's picture and bio"""

    class Meta:
        model = Profile
        fields = ["bio", "image"]




