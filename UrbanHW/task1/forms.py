from django import forms

class UserAuthentication(forms.Form):
    username = forms.CharField(max_length=30, label='введите логин')
    password = forms.CharField(widget=forms.PasswordInput(), min_length=8, label='Введите пароль')


class UserRegister(UserAuthentication):
    repeat_password = forms.CharField(widget=forms.PasswordInput(), min_length=8, label='Повторите пароль')
    age = forms.IntegerField(label='Введите свой возраст', min_value=1)

