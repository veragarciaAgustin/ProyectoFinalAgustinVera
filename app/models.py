from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
import os

# Create your models here.

def upload_to():
    return os.path.join('media/')

class Articulo(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = HTMLField()
    fecha = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=upload_to(), null=True)
    destacado = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

class Comentario(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comentario_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comentario_dislikes', blank=True)