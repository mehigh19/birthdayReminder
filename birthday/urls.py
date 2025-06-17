from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addBday', views.addBday, name='addBday'),
    path('addBdayHtml', views.addBdayHtml, name='addBday.html'),
    path('deleteBday', views.deleteBday, name='deleteBday'),
    path('editBday', views.editBday, name='editBday'),
    path('editBdayHtml', views.editBdayHtml, name='editBdayHtml'),
    path('upComing', views.upComing, name='upComing'),
    
]


