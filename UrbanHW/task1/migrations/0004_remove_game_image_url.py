# Generated by Django 5.1.2 on 2024-10-26 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0003_remove_game_link_to_purchase_buyer_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='image_url',
        ),
    ]
