# Generated by Django 5.1.1 on 2024-10-11 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_remove_servicio_comentarios_comentario_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogo',
            name='fondo_chatbot',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes'),
        ),
    ]
