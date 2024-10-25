# Generated by Django 5.1.1 on 2024-10-13 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_chatbot_x_chatbot_facebook_chatbot_instagram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbot',
            name='X',
            field=models.CharField(default='<a href="https://x.com/DesoftSsp" class="twitter">X <i class="bx bxl-twitter"></i></a>', max_length=255),
        ),
        migrations.AlterField(
            model_name='chatbot',
            name='facebook',
            field=models.CharField(default='<a href="https://www.facebook.com/SolucionesDTeam" class="facebook">facebook <i class="bx bxl-facebook"></i></a>', max_length=255),
        ),
        migrations.AlterField(
            model_name='chatbot',
            name='instagram',
            field=models.CharField(default='<a href="https://www.instagram.com/solucionesdteam/" class="instagram">instagram <i class="bx bxl-instagram"></i></a>', max_length=255),
        ),
        migrations.AlterField(
            model_name='chatbot',
            name='telegram',
            field=models.CharField(default='<a href="https://t.me/clientesDesoftSSP" class="telegram">telegram <i class="bx bxl-telegram"></i></a>', max_length=255),
        ),
        migrations.AlterField(
            model_name='chatbot',
            name='whatsapp',
            field=models.CharField(default='<a href="https://chat.whatsapp.com/GXwpDNRWs1F6NOM1Z2fzbc">whatsapp <i class="bx bxl-whatsapp"></i></a></a>', max_length=255),
        ),
    ]
