from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('load_claim_list/', views.load_claim_list, name='load_claim_list'),
    path('claim_list/', views.display_claim_list, name="display_claim_list")
]