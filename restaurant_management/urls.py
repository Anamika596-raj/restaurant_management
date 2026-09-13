from django.contrib import admin
from django.urls import path
from restaurant_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('orders/', views.my_orders, name='my_orders'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('dashboard/', views.dashboard, name='dashboard'),
]