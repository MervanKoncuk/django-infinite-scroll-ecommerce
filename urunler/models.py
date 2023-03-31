from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from user.models import *
# Create your models here.
class Kategori(models.Model):
    isim = models.CharField(max_length=100)
    kullanicilar = models.ManyToManyField(Profile)
    def __str__(self):
        return self.isim

class AltKategori(models.Model):
    isim = models.CharField(max_length=100)
    def __str__(self):
        return self.isim

class Tek(models.Model):
    isim = models.CharField(max_length=100)
    def __str__(self):
        return self.isim

class Urun(models.Model):
    olusturan = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, null=True) # SET_NULL
    sub_category = models.ManyToManyField(AltKategori)
    tekBilgi = models.OneToOneField(Tek, on_delete=models.CASCADE, null=True, blank=True)
    isim = models.CharField(max_length=100, verbose_name="Ürün ismi") # input type text
    aciklama = RichTextField(max_length=500, verbose_name="Ürün açıklaması") # textarea
    no = models.IntegerField(verbose_name="Ürün Fiyatı") # type number
    resim = models.FileField(upload_to='urunler/', null=True, blank=True, verbose_name="Ürün resmi") # type file
    def __str__(self):
        return self.isim
# django 
# foreignkey = manytoone
# manytomany
# onetoone
# ckeditor


# sepet için lazım olan bilgiler
# urun - foreignkey
# kullanici - foreignkey
# adet
# toplam fiyat
class Sepet(models.Model):
    urun = models.ForeignKey(Urun, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adet = models.IntegerField()
    toplam = models.IntegerField()
    odendiMi = models.BooleanField(default=False)

    def __str__(self):
        return self.urun.isim

class Odeme(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sepet = models.ManyToManyField(Sepet)
    toplamFiyat = models.IntegerField()
    odendiMi = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username