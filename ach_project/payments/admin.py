from django.contrib import admin
from .models import BankAccount, ACHEntry

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_holder_name', 'institution_name', 'account_type', 'is_verified')
    list_filter = ('account_type', 'is_verified')
    search_fields = ('account_holder_name', 'institution_name', 'account_number')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'account_holder_name', 'account_type')
        }),
        ('Bank Details', {
            'fields': ('routing_number', 'account_number', 'institution_name')
        }),
        ('Status', {
            'fields': ('is_verified', 'created_at')
        }),
    )

class ACHEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'source_account__account_number', 'destination_account__account_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'status')
        }),
        ('Transfer Details', {
            'fields': ('source_account', 'destination_account', 'amount', 'description')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# Register your models here
admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(ACHEntry, ACHEntryAdmin)