from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting
from order.models import ShopCartForm, ShopCart
from product.models import Category

def index(request):
    #setting = Setting.objects.get(pk=1)
    return HttpResponse("Order App")

@login_required(login_url='/login') #check login
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user #access user session information
    #****** ÜRÜN SEPETTE Mİ KONTROLÜ *******
    checkproduct=ShopCart.objects.filter(product_id=id) #ürün sepette mi?
    if checkproduct:
        control=1 #ürün sepette
    else:
        control=0 #ürün sepette değil

    if request.method == 'POST': #ÜRÜN DETAY SAYFASINDAN EKLE BUTONUNA BASINCA
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: #ürün varsa güncelle
                data=ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save() #db kaydı
            else: #ürün yoksa ekle
                data=ShopCart() #model ile bağlantı
                data.user_id=current_user.id
                data.product_id=id
                data.quantity = form.cleaned_data['quantity']
                data.save() #db kaydı

        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count() #listedekileri sayar
        messages.success(request,"Ürün eklenmiştir. Sporla Kalın!")
        return HttpResponseRedirect(url)

    else: #ANASAYFADAN EKLE BUTONUNA BASINCA
        if control == 1:  # ürün varsa güncelle
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()  # db kaydı
        else:  # ürün yoksa ekle
            data = ShopCart() # model ile bağlantı
            data.user_id = current_user.id
            data.product_id = id
            data.quantity=1
            data.save() # db kaydı

        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # listedekileri sayar
        messages.success(request, "Ürün eklenmiştir. Sporla Kalın!")
        return HttpResponseRedirect(url)

    messages.warning(request,"Ürün kaydı yapılamamıştır.")
    return  HttpResponseRedirect(url)

@login_required(login_url='/login') #check login
def shopcart(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # listedekileri sayar

    total=0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    context={'setting': setting,
             'shopcart': shopcart,
             'category':category,
             'total': total,
             }
    return render(request,'shopcart_products.html',context)


@login_required(login_url='/login') # Check login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user=request.user  # Access User Session information
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # listedekileri sayar
    messages.success(request, "Seçtiğiniz spor sepetten silinmiştir.")
    return HttpResponseRedirect("/shopcart")