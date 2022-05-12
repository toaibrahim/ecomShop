from .models import Newletter
from django import forms

class NewletterAdd(forms.ModelForm):
    class Meta:
        model = Newletter
        fields = "__all__"