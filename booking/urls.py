from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('book/', views.book_ticket, name='book_ticket'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('download/<int:booking_id>/', views.download_ticket, name='download_ticket'),
]