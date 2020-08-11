from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import Setting, UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from product.models import Category, Product


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

@login_required(login_url='/login')  # Check login
def orderproduct(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.all()
    current_user = request.user
    shopcart=ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total+= rs.product.price * rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        if form.is_valid():
            #kredi kartı bilgilerini bankaya gönder onay gelirse dewamkee
            #<*><*><*><*>#
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total=total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(8).upper() #random kod üretir
            data.code = ordercode
            data.save()

            #move shopcart items to order products items
            shopcart=ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id #order id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                detail.price        = rs.product.price
                detail.amount       = rs.amount
                detail.save()
                #***** reduce quantity of sold product from amount of product
                product=Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
                #****+++---*****

            ShopCart.objects.filter(user_id=current_user.id).delete() #Clear and Delete ShopCart
            request.session['cart_items']=0
            messages.success(request, "Üyeliğiniz başarıyla tamamlanmıştır. Sporla kalın! ")
            return render(request, 'Order_Completed.html', {'ordercode': ordercode,
                                                            'category': category,
                                                            'setting': setting})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct/")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'shopcart':shopcart,
               'form': form,
               'total': total,
               'profile': profile,
               'product': product,
               'setting': setting,
               }
    return render(request, 'Order_Form.html', context)