# Generated by Django 5.0.3 on 2024-04-15 14:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_articulo_imagen_comentario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentario',
            old_name='fecha_publicacion',
            new_name='fecha',
        ),
        migrations.RenameField(
            model_name='comentario',
            old_name='contenido',
            new_name='texto',
        ),
        migrations.RenameField(
            model_name='comentario',
            old_name='autor',
            new_name='usuario',
        ),
        migrations.AddField(
            model_name='comentario',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comentario_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]