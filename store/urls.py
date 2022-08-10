from django.urls import path

from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.HomeView, name='home'),
    path('product/', views.product, name="product"),
    path('login/', views.loginpage, name="login"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('register/', views.registerpage, name="register"),
    path('logout', views.logoutuser, name="logout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order', views.processOrder, name="process_order"),
    path('why_us', views.why_us, name="why_us"),
    path('product_details', views.product_details, name="product_details"),
    path('about', views.about, name="about")

]
