from django.urls import path, re_path

from . import views
from django.contrib.staticfiles import views as static

app_name = 'dbs'

urlpatterns = [
	path('', views.index, name='start'),
	path('index', views.index, name='index'),
	path('dbs_authorize', views.dbs_authorize, name='dbs_authorize'),
	path('account_balance', views.account_balance, name='account_balance'),
	path('dbs_connect_account', views.dbs_connect_account, name='dbs_connect_account'),
	path('ocbc_connect_account', views.ocbc_connect_account, name='ocbc_connect_account'),
	path('transfer', views.transfer, name='transfer'),
	path('payNow', views.payNow_transfer, name='payNow'),
	path('confirmation', views.payNow_transfer_lamp, name='confirmation'),
	path('transaction_history', views.transaction_history, name='transaction_history'),
	path('product_page', views.product_page, name='product_page'),
	path('payment_method', views.payment_method, name='payment_method'),
	path('paynow_maesh', views.paynow_maesh, name='paynow_maesh'),
	path('payment_maesh_dbs', views.payment_maesh, name='payment_maesh_dbs'),
	path('payment_maesh_ocbc', views.payment_maesh, name='payment_maesh_ocbc'),
]