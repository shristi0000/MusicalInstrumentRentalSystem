from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image
from .models import Instrument, RentInstruments
# from .models import Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text="Required. Enter a valid email address."
    )
    first_name = forms.CharField(
        max_length=30, required=True, help_text="Required. Enter your first name."
    )
    last_name = forms.CharField(
        max_length=30, required=True, help_text="Required. Enter your last name."
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ["name", "type", "price_per_day", "images", "description"]

    def save(self, commit: bool = ...) -> Any:
        return super().save(commit)


class RentForm(forms.ModelForm):
    class Meta:
        model = RentInstruments
        fields = [
            "id",
            "instrument",
            "renter",
            "pickup_date",
            "dropoff_date",
            "pickup_address",
            "dropoff_address",
            "status",
        ]

class ImagesForm(forms.ModelForm):
    pic = forms.FileField(widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label = "")
    class Meta:
        model = Image
        fields = ['images']

#     class CommentForm(forms.ModelForm):
#         content = forms.CharField(label ="", widget = forms.Textarea(
#     attrs ={
#         'class':'form-control',
#         'placeholder':'Comment here !',
#         'rows':4,
#         'cols':50
#     }))
#     class Meta:
#         model = Comment
#         fields =['content']