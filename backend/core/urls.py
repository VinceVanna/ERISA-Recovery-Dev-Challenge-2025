from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('load_claim_list/', views.load_claim_list, name='load_claim_list'),
    path('claim_list/', views.display_claim_list, name='display_claim_list'),
    path('load_claim_detail/', views.load_claim_detail, name='load_claim_detail'),
    path('claim_detail/', views.display_claim_detail, name='display_claim_detail'),
    path('search_detail/<int:claim_id>/', views.search_claim_detail, name='search_claim_detail'),
    path('navbar/', views.load_navbar, name='navbar'),
    path('login_card/', views.load_login_card, name='login_card'),
    path('register_card/', views.load_register_card, name='register_card'),
    path('register/', views.register_page, name='register'),
    path('create_employee/', views.create_employee, name='create_employee')
]