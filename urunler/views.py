from django.shortcuts import render, redirect
from .models import *
from .forms import *
import iyzipay
import json
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
from user.models import *
# paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

api_key = 'sandbox-alkEsAoGI9XkBDM6o2K5wMtkK0OsnE75'
secret_key = 'sandbox-pTuk2OVnG960y2vwLXt5FybQsrqM7aL5'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key':api_key,
    'secret_key':secret_key,
    'base_url':base_url
}

sozlukToken = list()


def payment(request):
    context = dict()
    odeme = Odeme.objects.get(user = request.user, odendiMi = False)
    buyer={
        'id': 'BY789',
        'name': odeme.user.username,
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': odeme.toplamFiyat,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(json_content["checkoutFormContent"])


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)

def success(request):
    odeme = Odeme.objects.get(user = request.user, odendiMi = False)
    odeme.odendiMi = True
    odeme.save()
    odenenler = Sepet.objects.filter(user = request.user, odendiMi = False)
    for i in odenenler:
        print(i)
        i.odendiMi = True
        i.save()
    messages.success(request, 'Ödeme Başarılı')
    return redirect('index')
def failure(request):
    messages.error(request, 'Ödeme Başarısız')
    return redirect('index')
# Create your views here.
def index(request):
    urunler = Urun.objects.all()
    kategoriler = Kategori.objects.all()
    profiller = ''
    profilkategori = ''
    if request.user.is_authenticated:
        profiller = Profile.objects.get(user = request.user)
        profilkategori = profiller.kategori_set.all()
    for i in profilkategori:
        print(i.urun_set.all())
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        urunler = Urun.objects.filter(
            Q(isim__icontains = search) | # altgr + -
            Q(kategori__isim__icontains = search)
        )

    if request.method == "POST":
        if request.user.is_authenticated:
            urunId = request.POST['urunId']
            adet = request.POST['adet']
            urunum = Urun.objects.get(id = urunId)
            if Sepet.objects.filter(user = request.user, urun = urunum, odendiMi = False).exists():
                sepetim = Sepet.objects.get(user = request.user, urun = urunum)
                sepetim.adet += int(adet)
                sepetim.toplam = urunum.no * int(sepetim.adet)
                sepetim.save()
                return redirect('index')
            else:
                sepetim = Sepet.objects.create(
                    urun = urunum,
                    user = request.user,
                    adet = adet,
                    toplam = urunum.no * int(adet)
                )
                sepetim.save()
                return redirect('index')
        else:
            messages.info(request, 'ürün ekleyebilmek giriş yapmanız gerekmektedir')
            return redirect('login')
    if request.user.is_authenticated:
        sepetAdet = Sepet.objects.filter(user = request.user).count()
    else:
        sepetAdet = 0
    # pagination
    paginator = Paginator(urunler, 3)
    page = request.GET.get('page')
    urunler = paginator.get_page(page)  

    context = {
        'urunler':urunler,
        'search':search,
        'kategoriler':kategoriler,
        'sepetAdet':sepetAdet,
        'profiller':profiller,
        'paginator':paginator,
    }
    return render(request, 'index.html', context)

def hakkimda(request):
    # print(request)
    return render(request, 'hakkimda.html')

def urun(request, urunId):
    product = Urun.objects.filter(id = urunId)
    print(product)
    context = {
        'urun':product
    }
    # sozluk = {
    #     'isim': ['ahmet', 'Mehmet', 'Mustafa']
    # }
    # for i in sozluk['isim']:
    #     print(i)
    return render(request, 'urun.html', context)

def olustur(request):
    form = UrunForm()
    if request.method == 'POST':
        form = UrunForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            # Olusturan bilgisini doldurmak için
            user = form.save(commit = False)
            user.olusturan = request.user # request.user = Girişli olan kullanıcı
            user.save()
            messages.success(request, 'Ürün oluşturuldu')
            return redirect('index')
    context = {
        'form':form
    }
    return render(request, 'olustur.html', context)


def urunlerim(request):
    urunler = Urun.objects.filter(olusturan = request.user)
    if request.method == 'POST':
        sil = request.POST['sil']

        urun = Urun.objects.get(id = sil)
        urun.delete()
        messages.success(request, 'Ürün silindi')
        return redirect('urunlerim')
    context = {
        'urunler':urunler
    }
    return render(request, 'urunlerim.html', context)

def sepet(request):
    urunler = Sepet.objects.filter(user = request.user)
    toplam = 0
    for i in urunler:
        print(i.toplam)
        toplam += i.toplam
        print("t = ",toplam)
    if 'sil' in request.POST:
        sil = request.POST['sil']
        print("a")
        urun = Sepet.objects.get(id = sil)
        urun.delete()
        messages.success(request, 'Ürün sepetten kaldırıldı')
        return redirect('sepet')
    if 'toplam' in request.POST:
        toplam = request.POST['toplam']
        odenen = Sepet.objects.filter(user = request.user)

        if Odeme.objects.filter(user = request.user, odendiMi = False).exists():
            odemeYap = Odeme.objects.get(user = request.user, odendiMi = False)
            odemeYap.toplamFiyat = toplam
            odemeYap.sepet.add(*odenen)
            odemeYap.save()
            return redirect('payment')
        else:
            odemeYap = Odeme.objects.create(
                user = request.user,
                toplamFiyat = toplam,
                
            )
            odemeYap.sepet.add(*odenen)
            odemeYap.save()
            return redirect('payment')
    context = {
        'urunler':urunler,
        'toplam':toplam
    }
    return render(request, 'sepet.html', context)