# Generated by Django 5.1.1 on 2024-10-30 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_catalogo_fondo_login_mobile_catalogo_fondo_login_pc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Correos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo1', models.EmailField(max_length=254)),
                ('correo2', models.EmailField(max_length=254)),
                ('correo3', models.EmailField(max_length=254)),
                ('correo4', models.EmailField(max_length=254)),
                ('correo5', models.EmailField(max_length=254)),
                ('correo6', models.EmailField(max_length=254)),
                ('correo7', models.EmailField(max_length=254)),
                ('correo8', models.EmailField(max_length=254)),
                ('correo9', models.EmailField(max_length=254)),
                ('correo10', models.EmailField(max_length=254)),
            ],
        ),
    ]
