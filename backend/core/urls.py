from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('load_claim_list/', views.load_claim_list, name='load_claim_list'),
    path('claim_list/', views.display_claim_list, name='display_claim_list'),
    path('load_claim_detail/', views.load_claim_detail, name='load_claim_detail'),
    path('search_detail/<int:claim_id>/', views.search_claim_detail, name='search_claim_detail'),
    path('navbar/', views.load_navbar, name='navbar'),
    path('login_card/', views.load_login_card, name='login_card'),
    path('register_card/', views.load_register_card, name='register_card'),
    path('register/', views.register_page, name='register'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('employee_logout/', views.employee_logout, name='employee_logout'),
    path('toggle_flag/<int:claim_id>/', views.toggle_flag, name='toggle_flag'),
    path('save_annotation/', views.save_annotation, name="save_annotation"),
    path('get_annotation/<int:claim_id>/', views.get_annotation, name='get_annotation'),
    path('save_note/', views.save_note, name='save_note'),
    path('get_note/<int:claim_id>/', views.get_note, name='get_note'),
    path('get_employee/', views.get_employee, name="get_employee"),
    path('display_employee/', views.display_employee, name="load_employee"),
    path('get_flagged/', views.get_all_flag, name="get_all_flag"),
    path('display_flag/', views.display_flag, name="load_flag"),
    path('get_note/', views.get_all_note, name="get_all_note"),
    path('display_note/', views.display_note, name="load_note"),
    path('get_annotation/', views.get_all_annotation, name="get_all_annotation"),
    path('display_annotation/', views.display_annotation, name="load_annotation"),
    path('flag_count/', views.count_flagged, name="flag_count"),
    path('underpayment/', views.get_underpayment, name="underpayment"),
    path('admin_dashboard/', views.load_dashboard, name="load_dashboard"),
    path('back_button/', views.load_back_button, name ="back_button")
]