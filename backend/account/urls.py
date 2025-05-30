from django.urls import path
from . import views

urlpatterns = [
    path('new-invoice', views.create_invoice_view, name='create_invoice'),
    path('<str:identity_card_number>/', views.get_customer_invoices_view, name='get_customer_invoices'),
    path('<str:identity_card_number>/amount_owed/', views.get_customer_amount_owed, name='get_customer_amount_owed'),
    path('<int:invoice_id>/pay/', views.pay_invoice_view, name='pay_invoice'),
]