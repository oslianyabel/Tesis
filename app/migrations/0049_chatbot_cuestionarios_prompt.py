# Generated by Django 5.1.1 on 2024-10-20 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_chatbot_generales_prompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbot',
            name='cuestionarios_prompt',
            field=models.TextField(default='Entrega al usuario un enlace de descarga de un modelo de cuestionario para solicitar un servicio dado.'),
        ),
    ]
