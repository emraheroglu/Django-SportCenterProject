from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting, UserProfile
from product.models import Category


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'setting': setting,
               'profile': profile
               }

    return render(request, "userprofile.html",context)