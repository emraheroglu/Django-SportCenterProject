"""sportscenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    path('', include('home.urls')), #path de bir şey yazmadan home çalıştırır
    path('home/', include('home.urls')),
    path('index/', views.index, name='index'),
    path('hakkimizda/', views.hakkimizda, name='hakkimizda'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('referanslar/', views.referanslar, name='referanslar'),
    path('blog/', views.blog, name='blog'),
    path('singleblog/', views.singleblog, name='singleblog'),
    path('galeri/', views.galeri, name='galeri'),
    path('fiyatlar/', views.fiyatlar, name='fiyatlar'),
    path('join/', views.join, name='join'),
    #path('branslar/', views.branslar, name='branslar'),
    path('login/', views.login, name='login'),
    path('product/', include('product.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>/', views.products, name='category_products'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
