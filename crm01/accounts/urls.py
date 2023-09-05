from django.urls import path
from . import views

urlpatterns = [
path('register/', views.register, name="register"),
path('login/', views.login, name="login"),
path('logout/', views.logoutUser, name="logout"),
path('profile/', views.profile_settings, name="profile"),
path('', views.home, name="home"),
path('cart/', views.cart, name="cart"),
path('checkout/', views.checkout, name="checkout"),
path('dashboard/', views.dashboard, name="dashboard"),

path('update_item/', views.updateItem, name="update_item"),
path('process_order/', views.processOrder, name="process_order"),

]