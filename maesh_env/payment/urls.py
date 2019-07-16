from django.urls import path, re_path

from . import views
from django.contrib.staticfiles import views as static

app_name = 'payment'

urlpatterns = [
	path('', views.product_page, name='start'),
	path('index', views.index, name='index'),
	path('account_balance', views.account_balance, name='account_balance'),
	path('transaction_history', views.transaction_history, name='transaction_history'),
	path('authorize', views.authorize, name='authorize'),
	re_path(r'^connect_bank/(?P<bank>.*)/$', views.connect_bank, name='connect_bank'),
	path('transfer', views.transfer, name='transfer'),
	path('confirmation', views.payNow_transfer, name='confirmation'),
	path('confirmed', views.confirmed, name='confirmed'),
	path('product_page', views.product_page, name='product_page'),
	path('payment_method', views.payment_method, name='payment_method'),
	path('paynow_maesh', views.paynow_maesh, name='paynow_maesh'),
	path('payment_maesh_dbs', views.payment_maesh, name='payment_maesh_dbs'),
	path('payment_maesh_ocbc', views.payment_maesh, name='payment_maesh_ocbc'),
	path('payment_maesh_citi', views.payment_maesh, name='payment_maesh_citi')
]