from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('', views.index, name="index"),  # function name is index or not
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('profile/', views.profile, name="profile"),
    path('checkout/', views.checkout, name="checkout"),
    path('handlerequest/', views.handlerequest, name="handlerequest"),
]



