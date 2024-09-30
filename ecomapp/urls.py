from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name= "home" ),
    path("about/", views.about, name="about"),
    path("shop/", views.shop, name="shop"),
    path("signup/", views.userForm, name="signup"),
    path("login/", views.login, name="login"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("cart/", views.cart_view, name="view_cart"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
]