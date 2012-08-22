# coding: latin1
from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(label="Nombre de Usuario")
    password=forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='required'
        self.fields['password'].widget.attrs['class']='required'

