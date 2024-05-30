from django import forms
from blogapp.models import post,authors,category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Postform(forms.ModelForm):
    class Meta:
        model=post
        fields=('title','content','thumbnail','categories','author')

class Signup(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)
    class Meta:
        model=User
        model._meta.get_field('email')._unique=True
        fields=('username','first_name','last_name','email','password1','password2')

class Authorform(forms.ModelForm):
    class Meta:
        model=authors
        fields="__all__"
class CategoryForm(forms.ModelForm):
    class Meta:
        model=category
        fields='__all__'

