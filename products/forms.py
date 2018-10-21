from django import forms

class SearchBar(forms.Form):
    content = forms.CharField(max_length=150)