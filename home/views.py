import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from home.models import Setting, ContactFormMessage, ContactFormu, UserProfile, SSS
from order.models import ShopCart
from product.models import Category, Product, Images, Comment
from home.forms import SearchForm, JoinForm


def index(request):
    current_user = request.user  # Access User Session information
    setting = Setting.objects.get(pk=1)
    sliderData = Product.objects.all().order_by('?')[:4]
    category = Category.objects.all()
    randomurunler = Product.objects.all().order_by('?')[:6]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # listedekileri sayar

    context = {'setting': setting,
               'page': 'home',
               'category': category,
               'sliderData': sliderData,
               'randomurunler': randomurunler,
               }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               'page': 'hakkimizda'
               }
    return render(request, 'hakkimizda.html', context)

def footer(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               }
    return render(request, 'footer.html', context)

def iletisim(request):
    # formu kaydetmek için bu fonksiyon yazıldı
    if request.method == 'POST':  # form post ediliyor
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarı ile gönderilmiştir, Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')

    # forma ulaşmak için bu kodlar yazıldı
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactFormu()
    context = {'setting': setting,
               'category': category,
               'form': form
               }
    return render(request, 'iletisim.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'category': category,
               'page': 'referanslar'
               }
    return render(request, 'referanslar.html', context)

def galeri(request):
    resimler = Product.objects.all().order_by('?')[:12]
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               'resimler':resimler,
               'page': 'galeri'
               }
    return render(request, 'galeri.html', context)

def fiyatlar(request):
    category = Category.objects.all()
    products=Product.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               'page': 'fiyatlar',
               'products': products,
               }
    return render(request, 'fiyatlar.html', context)

def join(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               'page': 'join'
               }
    return render(request, 'join.html', context)

def products(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products= Product.objects.filter(category_id=id)
    context = { 'products': products,
                'category': category,
                'categorydata': categorydata,
                'setting': setting,
               }
    return render(request,'products.html',context)

def product_detail(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'product': product,
               'category': category,
               'images': images,
               'comments': comments,
               'setting': setting,

               }
    return render(request, 'product_detail.html', context)

def product_search(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)  # Get form data
        if form.is_valid(): #formda herhangi bir aktivite var mı, geçerli mi(eylem)
            category = Category.objects.all()

            query = form.cleaned_data['query']  # Get form data  -- verileri kaydet
            catid = form.cleaned_data['catid']  # Get form data  -- kontrol edilecek veriyi al

            if catid == 0:
                products = Product.objects.filter(
                    title__icontains=query)  # Select * from product where title like %query%
            else:
                products = Product.objects.filter(
                    title__icontains=query, category_id=catid)
            # return HttpResponse(products)
            context = {'products': products,
                       'category': category,
                       'setting': setting,
                       }
            return render(request, 'products_search.html', context)
    return HttpResponseRedirect('/')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı yada şifre yanlış")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category,
        'setting': setting,
               }
    return render(request, 'login.html', context)

def join_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'images/users/manager.png'
            data.save()
            messages.success(request, "Hoş Geldin. Spor yapmak için harika bir gün değil mi?")
            return HttpResponseRedirect('/')

    form = JoinForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               'setting': setting,
               }

    return render(request, 'join.html', context)

def sss(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    sss = SSS.objects.all().order_by('ordernumber')
    context = {'category': category,
               'sss': sss,
               'setting': setting,
               }
    return render(request, 'sss.html', context)
