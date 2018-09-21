from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import UserProfile,Post
from django.forms.widgets import SelectDateWidget

class Edit(forms.ModelForm):
    user_profile = forms.ImageField(required=True)
    Birthdate = forms.DateField(required=True,input_formats=['%b %d, %Y'])
    class Meta:
        model = UserProfile
        fields = [
            'user_profile',
            'Birthdate',
            'about',
        ]
    def clean(self, commit=True):
        print(self.cleaned_data)
        return self.cleaned_data

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name =forms.CharField(required=True)
    last_name =forms.CharField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def clean(self, commit=True):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            self._errors["password"] = ["do not match"]
            del self.cleaned_data['password']
        return self.cleaned_data

class Post_Con(forms.ModelForm):
    post_img = forms.ImageField(required=True)
    post_msg = forms.CharField(required=False)
    post_date = forms.DateField(required=False,input_formats=['%b %d, %Y'])
    post_time = forms.TimeField(required=False,input_formats=['%I:%M %p'])

    class Meta:
        model = Post
        fields = [
            'post_img',
            'post_msg',
            'post_date',
            'post_time',
        ]
 


    
            