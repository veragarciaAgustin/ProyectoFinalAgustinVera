from django import forms
from tinymce.widgets import TinyMCE
from .models import Articulo

class ArticuloForm(forms.ModelForm):
    imagen = forms.ImageField(required=False)
    contenido = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'imagen']


