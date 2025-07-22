# admin.py
from django.contrib import admin
from rewards.models import Wallet
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

User = get_user_model()

class WalletInline(admin.StackedInline):
    model = Wallet
    can_delete = False
    verbose_name_plural = 'Wallet'
    fields = ('balance', 'last_updated',)
    readonly_fields = ('last_updated',)
    extra = 0

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = (WalletInline,)
    list_display = ('first_name', 'last_name', 'email',
                   'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ("phone",)
    
    fieldsets = (
        (None, {'fields': ("phone", "referred_by")}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',
                      'phone_number', 'first_name', 'last_name'),
        }),
    )
    
    def get_inline_instances(self, request, obj=None):
        # Only show wallet inline when editing an existing user
        if obj:
            return super().get_inline_instances(request, obj)
        return []

# # Register custom User with Wallet inline
# admin.site.register(User, UserAdmin)

# Register Wallet separately as well
# @admin.register(Wallet)
# class WalletAdmin(admin.ModelAdmin):
#     list_display = ('user', 'balance', 'last_updated')
#     list_select_related = ('user',)
#     search_fields = ('user__phone', 'user__email')
#     readonly_fields = ('last_updated',)
#     list_filter = ('user', 'last_updated')

# @admin.register(User)
# class UserAdmin(DjangoUserAdmin):
#     list_display = ('phone', 'email', 'referred_by')
#     search_fields = ('user__phone', 'user__email')
#     ordering = ("phone",)