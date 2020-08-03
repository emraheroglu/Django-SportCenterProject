from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from home.models import Setting


def index(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'home'}
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def iletisim(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'iletisim'}
    return render(request, 'iletisim.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'referanslar'}
    return render(request, 'referanslar.html', context)

def blog(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'blog'}
    return render(request, 'blog.html', context)

def singleblog(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'singleblog'}
    return render(request, 'singleblog.html', context)

def galeri(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'galeri'}
    return render(request, 'galeri.html', context)

def fiyatlar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'page':'fiyatlar'}
    return render(request, 'fiyatlar.html', context)