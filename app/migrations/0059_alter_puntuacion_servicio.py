# Generated by Django 5.1.1 on 2024-11-03 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_puntuacion_servicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntuacion',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.servicio'),
        ),
    ]