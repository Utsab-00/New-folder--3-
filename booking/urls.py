from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_ticket, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]