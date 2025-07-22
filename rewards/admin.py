# admin.py - Admin interface for wallet reward system

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from .models import (
    Wallet, 
    WalletTransaction, 
    WalletRewardConfiguration, 
    PendingWalletReward,
    # User
)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'pending_balance', 'total_transactions', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['user__phone', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['balance', 'pending_balance', 'last_updated', 'transaction_history']
    
    def total_transactions(self, obj):
        return obj.transactions.count()
    total_transactions.short_description = 'Total Transactions'
    
    def transaction_history(self, obj):
        transactions = obj.transactions.order_by('-created_at')[:10]
        html = '<table style="width:100%"><tr><th>Date</th><th>Type</th><th>Amount</th><th>Status</th><th>Description</th></tr>'
        for txn in transactions:
            html += f'<tr><td>{txn.created_at.strftime("%Y-%m-%d %H:%M")}</td><td>{txn.transaction_type}</td><td>${txn.amount}</td><td>{txn.status}</td><td>{txn.description}</td></tr>'
        html += '</table>'
        return mark_safe(html)
    transaction_history.short_description = 'Recent Transactions'


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet_user', 'transaction_type', 'amount', 'status', 'order_number', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['wallet__user__phone', 'order_number', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def wallet_user(self, obj):
        return obj.wallet.user
    wallet_user.short_description = 'User'
    wallet_user.admin_order_field = 'wallet__user'


@admin.register(WalletRewardConfiguration)
class WalletRewardConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer_reward_percentage', 'referrer_reward_percentage', 'minimum_order_value', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active')
        }),
        ('Reward Percentages', {
            'fields': ('customer_reward_percentage', 'referrer_reward_percentage', 'minimum_order_value')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        # Ensure only one active configuration
        if obj.is_active:
            WalletRewardConfiguration.objects.filter(is_active=True).update(is_active=False)
        super().save_model(request, obj, form, change)


@admin.register(PendingWalletReward)
class PendingWalletRewardAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_user', 'customer_reward_amount', 'referrer_user', 'referrer_reward_amount',  'created_at']
    list_filter = ['created_at']
    search_fields = ['order__number', 'order__user__phone', 'referrer__phone']
    readonly_fields = ['created_at', 'order_link', 'customer_wallet_link', 'referrer_wallet_link']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_link',)
        }),
        ('Customer Reward', {
            'fields': ('customer_reward_amount', 'customer_wallet_link')
        }),
        ('Referrer Reward', {
            'fields': ('referrer_user', 'referrer_reward_amount', 'referrer_wallet_link')
        }),
        ('Configuration', {
            'fields': ('configuration_used',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def order_number(self, obj):
        return obj.order.number
    order_number.short_description = 'Order Number'
    order_number.admin_order_field = 'order__number'
    
    def customer_user(self, obj):
        return obj.order.user
    customer_user.short_description = 'Customer'
    customer_user.admin_order_field = 'order__user'
    
    def referrer_user(self, obj):
        return obj.referrer or '-'
    referrer_user.short_description = 'Referrer'
    referrer_user.admin_order_field = 'referrer'
    
    def order_link(self, obj):
        url = reverse('admin:order_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.number)
    order_link.short_description = 'Order'
    
    def customer_wallet_link(self, obj):
        try:
            wallet = obj.order.user.wallet
            url = reverse('admin:yourapp_wallet_change', args=[wallet.pk])  # Replace 'yourapp' with your app name
            return format_html('<a href="{}">${}</a>', url, wallet.balance)
        except:
            return '-'
    customer_wallet_link.short_description = 'Customer Wallet'
    
    def referrer_wallet_link(self, obj):
        if obj.referrer:
            try:
                wallet = obj.referrer.wallet
                url = reverse('admin:yourapp_wallet_change', args=[wallet.pk])  # Replace 'yourapp' with your app name
                return format_html('<a href="{}">${}</a>', url, wallet.balance)
            except:
                return '-'
        return