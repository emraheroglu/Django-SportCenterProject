from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.deletecomment, name="deletecomment"),
    path('memberships/', views.orders, name="orders"),
    path('orderdetail/<int:id>', views.orderdetail, name="orderdetail"),
]