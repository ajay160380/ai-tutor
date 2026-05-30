from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CLASS_CHOICES, EXAM_CHOICES


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'your@email.com'})
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Last Name'})
    )
    student_class = forms.ChoiceField(
        choices=CLASS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-control-custom'})
    )
    target_exam = forms.CharField(
        widget=forms.HiddenInput(),
        initial='BOARD'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-custom',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-custom',
            'placeholder': 'Create password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-custom',
            'placeholder': 'Confirm password'
        })


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-custom',
            'placeholder': 'Username ya Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-custom',
            'placeholder': 'Password'
        })
    )
