from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
# from .views import CustomLoginView

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path("login/", views.login_request, name="login"),
path("logout", views.logout_request, name="logout"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name = "update_item"),
path('process_order/', views.processOrder, name = "process_order"),

]