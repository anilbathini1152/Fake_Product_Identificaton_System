from django import forms
from .models import *
  
class QRForm(forms.ModelForm):
    QR = forms.CharField(max_length=50)
    file = forms.FileField()
    class Meta:
        model = QRUp
        fields = ['qr_img']