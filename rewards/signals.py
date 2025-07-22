# signals.py - Order processing signals for wallet rewards

from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from oscar.apps.order.signals import order_placed, order_status_changed
from oscar.apps.order.models import Order, OrderStatusChange
from oscar.core.loading import get_model
from .models import (
    WalletRewardConfiguration,
    PendingWalletReward, 
    Wallet 
)
from user.models import User    


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=100)


@receiver(order_placed)
def create_pending_wallet_reward(sender, order, **kwargs):
    config = WalletRewardConfiguration.get_active_config()
    if not config:
        return
    
    if order.total_incl_tax < config.minimum_order_value:
        return
    
    customer_reward = (order.total_incl_tax * config.customer_reward_percentage) / 100
    referrer_reward = Decimal('0.00')
    referrer = None
    
    if order.user.referred_by:
        referrer = order.user.referred_by
        referrer_reward = (order.total_incl_tax * config.referrer_reward_percentage) / 100
    
    PendingWalletReward.objects.create(
        order=order,
        customer_reward_amount=customer_reward,
        referrer_reward_amount=referrer_reward,
        referrer=referrer,
        configuration_used=config
    )


@receiver(order_status_changed)
def handle_order_status_change(sender, order, old_status, new_status, **kwargs):
    try:
        pending_reward = PendingWalletReward.objects.get(order=order)
    except PendingWalletReward.DoesNotExist:
        print(f"No pending reward found for order {order.number}")
        return
    
    if pending_reward.status == 'PENDING':
        if new_status == 'Delivered':
            pending_reward.confirm_reward()
        elif new_status == 'Cancelled':
            pending_reward.cancel_reward()
    
