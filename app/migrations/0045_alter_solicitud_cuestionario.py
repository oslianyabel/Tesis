# Generated by Django 5.1.1 on 2024-10-17 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_solicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='cuestionario',
            field=models.TextField(),
        ),
    ]
