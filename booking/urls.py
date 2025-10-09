from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_ticket, name='book_ticket'),
    path('dashboard/', views.dashboard, name='dashboard'),
]