from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    text = "Merhaba Django!<br>Meğhaba Fenebahci"
    context = {'text': text}
    return render(request, 'index.html', context)