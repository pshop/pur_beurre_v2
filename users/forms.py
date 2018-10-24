from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Entrez un nom d'utilisateur")
    email = forms.EmailField(label="Entrez votre adresse mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password_check = forms.CharField(label="Entrez à nouveau votre mot de passe", widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.CharField(max_length=150, label="Entrez votre adresse mail")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)