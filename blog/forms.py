from django.forms import ModelForm
from .models import Place, Review, Like
from django.contrib.auth.models import User


class CreatePlace(ModelForm):
    """This form will receive information to create a new place to review it."""

    class Meta:
        model = Place
        fields = ["name", "address", "phone", "description", "image"]

class ReviewForm(ModelForm):
    """This is the form to create a new review"""

    class Meta:
        model = Review
        fields = ["description"]




