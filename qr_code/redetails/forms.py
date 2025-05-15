from django import forms
from .models import *

class QRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['data']



class QRCodeForm2(forms.ModelForm):
    class Meta:
        model = QRCode2
        fields = ['name', 'address', 'email', 'contact', 'extra_image', 'data']
