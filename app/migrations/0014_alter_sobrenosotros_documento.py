# Generated by Django 4.2.16 on 2024-10-03 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_sobrenosotros_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sobrenosotros',
            name='documento',
            field=models.FileField(upload_to='../app/static/app/'),
        ),
    ]
