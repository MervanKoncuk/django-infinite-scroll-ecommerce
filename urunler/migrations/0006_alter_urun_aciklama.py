# Generated by Django 3.2.12 on 2022-11-03 17:44

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urunler', '0005_auto_20221103_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urun',
            name='aciklama',
            field=ckeditor.fields.RichTextField(max_length=500, verbose_name='Ürün açıklaması'),
        ),
    ]