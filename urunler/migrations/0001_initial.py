# Generated by Django 3.2.12 on 2022-10-20 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=100)),
                ('aciklama', models.TextField(max_length=500)),
                ('no', models.IntegerField()),
            ],
        ),
    ]
