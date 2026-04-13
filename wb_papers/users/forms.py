from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# usercreation Form -> Ready made from in django that has fields: username,email,password1, password2 etc.

class SignUpForm(UserCreationForm):
    # Inherit everything from UserCreationForm plus my custom email field
    email = forms.EmailField(required=True, help_text="Use @college.ac.in for Faculty")
    
    class Meta(UserCreationForm.Meta):
        # model = User  -> This is already written in UserCreationForm,so we didnt have to write any model,data will be saved in User Table by default
        fields = UserCreationForm.Meta.fields + ('email',)