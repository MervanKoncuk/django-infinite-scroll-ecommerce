# Generated by Django 4.1.3 on 2022-11-08 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urunler', '0006_alter_urun_aciklama'),
    ]

    operations = [
        migrations.AddField(
            model_name='urun',
            name='olusturan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]