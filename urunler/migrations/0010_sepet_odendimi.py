# Generated by Django 4.1.3 on 2022-12-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urunler', '0009_odeme'),
    ]

    operations = [
        migrations.AddField(
            model_name='sepet',
            name='odendiMi',
            field=models.BooleanField(default=False),
        ),
    ]
