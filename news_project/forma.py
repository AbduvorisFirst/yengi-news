from django import forms
from .models import Category, New, Subscribe, Contact


class Form(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class FormNew(forms.ModelForm):
    class Meta:
        model = New
        fields = "__all__"

class FormSubs(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = "__all__"

class FormCon(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"