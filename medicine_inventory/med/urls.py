from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home),
    # path('/home',views.home),
    path("purchase/",views.purchase),
    path("stock/",views.stock),
    path("sales/",views.sales),
    path("generate_pdf/",views.generate_pdf,name='generate_pdf'),
]
