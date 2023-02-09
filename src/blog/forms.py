from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput
from blog import models


RATES = (
    ("1", "1"),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))
    password = forms.CharField(max_length=63, widget=PasswordInput(attrs={'placeholder': 'Mot de passe'}), label="")


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
        widgets = {'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'label':''}),
                   'password1': forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'label': ''}),
                   'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe', 'label': ''})
                   }


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widget = {'rating': forms.RadioSelect(attrs={'class': 'rating'})}