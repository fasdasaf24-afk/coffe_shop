from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.all_menu, name='menu'),
    path('menu/<str:category_slug>/', views.all_menu, name='menu_category'),
    path('new/', views.new_items, name='new'),
    path('delivery/', views.delivery, name='delivery'),
    path('locations/', views.locations, name='locations'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/decrease/<int:product_id>/', views.decrease_from_cart, name='decrease_from_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/support/', views.send_support_message, name='send_support_message'),
]
