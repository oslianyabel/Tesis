# Generated by Django 4.2.16 on 2024-10-03 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_equipo_apellido_alter_equipo_cargo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='apellido',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='cargo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
