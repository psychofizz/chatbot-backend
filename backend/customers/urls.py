from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.customer_list_create, name='customer_list_create_api'),
    path('customers/<str:identity_card_number>/', views.customer_detail_update_delete, name='customer_detail_by_id_card'),
]
