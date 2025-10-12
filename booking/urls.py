from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.book_ticket, name='book_ticket'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/<int:booking_id>/', views.download_ticket, name='download_ticket'),
    path('preview/<int:booking_id>/', views.preview_ticket, name='preview_ticket'),
]