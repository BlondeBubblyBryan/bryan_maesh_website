from django.contrib import admin

from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','company_name','paid','transaction_id','reference_code','amount', 'currency', 'UEN')

admin.site.register(Transaction, TransactionAdmin)