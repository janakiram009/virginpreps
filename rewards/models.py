from oscar.core.loading import get_model
from django.utils import timezone
from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from decimal import Decimal     

# Get Oscar models
Order = get_model('order', 'Order')
User = get_user_model() 

class OrderPolicyConfiguration(models.Model):
    cancel_return_period_days = models.PositiveIntegerField(default=7, help_text="Number of days allowed for cancellation/return after order placement.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order Policy Configuration"
        verbose_name_plural = "Order Policy Configurations"

    def __str__(self):
        return f"Cancel/Return Period: {self.cancel_return_period_days} days"

    @classmethod
    def get_period(cls):
        config = cls.objects.first()
        return config.cancel_return_period_days if config else 7

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    pending_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    last_updated = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Wallet, self).__init__(*args, **kwargs)
        pending_rewards = PendingWalletReward.objects.filter(order__user=self.user)
        total1 = pending_rewards.aggregate(total=models.Sum('customer_reward_amount'))['total'] or 0.00
        pending_rewards = PendingWalletReward.objects.filter(referrer=self.user)
        total2 = pending_rewards.aggregate(total=models.Sum('referrer_reward_amount'))['total'] or 0.00
        self.pending_balance = total1 + total2
        
    @transaction.atomic
    def credit(self, amount, order_number, description=None,  status='CONFIRMED'):
        if amount <= 0:
            raise ValidationError("Credit amount must be positive")
        self.balance += amount
        self.save()

        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='CREDIT',
            description=description,
            order_number=order_number,
            status=status
        )
   
    @transaction.atomic
    def debit(self, amount, order_number, description=None, status='CANCELLED'):
        if amount <= 0:
            raise ValidationError("Debit amount must be positive")
        if self.balance < amount:
            raise ValidationError("Insufficient balance")
        self.balance -= amount
        self.save()

        WalletTransaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type='DEBIT',
            description=description,
            order_number=order_number,
            status='CANCELLED'
        )

    # @transaction.atomic
    # def confirm_pending_credit(self, order_number):
    #     """Confirm pending credits when order is completed"""
    #     pending_transactions = self.transactions.filter(
    #         transaction_type='CREDIT',
    #         status='PENDING',
    #         order_number=order_number
    #     )
        
    #     total_pending = sum(t.amount for t in pending_transactions)
    #     if total_pending > 0:
    #         self.balance += total_pending
    #         self.pending_balance -= total_pending
    #         self.save()
            
    #         pending_transactions.update(status='CONFIRMED')

    # @transaction.atomic
    # def cancel_pending_credit(self, order_number):
    #     """Cancel pending credits when order is cancelled/returned"""
    #     pending_transactions = self.transactions.filter(
    #         transaction_type='CREDIT',
    #         status='PENDING',
    #         order_number=order_number
    #     )
        
    #     total_pending = sum(t.amount for t in pending_transactions)
    #     if total_pending > 0:
    #         self.pending_balance -= total_pending
    #         self.save()
            
    #         pending_transactions.update(status='CANCELLED')

    def __str__(self):
        return f"{self.user.username}'s Wallet: ${self.balance} (Pending: ${self.pending_balance})"


class WalletTransaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('CREDIT', 'Credit'), ('DEBIT', 'Debit')])
    description = models.CharField(max_length=255)
    order_number = models.CharField(max_length=128, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of ${self.amount} for {self.wallet.user.username} ({self.status})"


class WalletRewardConfiguration(models.Model):
    """Model to store dynamic wallet reward percentages"""
    name = models.CharField(max_length=100, unique=True)
    customer_reward_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0.00)],
        help_text="Percentage of order value to credit to customer's wallet"
    )
    referrer_reward_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(0.00)],
        help_text="Percentage of order value to credit to referrer's wallet"
    )
    minimum_order_value = models.DecimalField(
        max_digits=10, decimal_places=2, 
        default=0.00,
        help_text="Minimum order value to qualify for rewards"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wallet Reward Configuration"
        verbose_name_plural = "Wallet Reward Configurations"

    def __str__(self):
        return f"{self.name} - Customer: {self.customer_reward_percentage}%, Referrer: {self.referrer_reward_percentage}%"

    @classmethod
    def get_active_config(cls):
        """Get the active configuration"""
        return cls.objects.filter(is_active=True).first()


class PendingWalletReward(models.Model):
    """Track pending wallet rewards for orders"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='pending_wallet_reward')
    customer_reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referrer_reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pending_referrer_rewards')
    configuration_used = models.ForeignKey(WalletRewardConfiguration, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled'),
            # ('PARTIALLY_RETURNED', 'Partially Returned'),
        ],
        default='PENDING'
    )

    def confirm_reward(self):
        """Confirm the reward after order delivered"""
        if self.status != 'PENDING':
            print(f"Cannot confirm reward for order {self.order.number} as it is not pending.")
            return
        
        with transaction.atomic():
            if self.customer_reward_amount > 0:
                customer_wallet = self.order.user.wallet
                customer_wallet.credit(self.customer_reward_amount, self.order.number)
            
            if self.referrer and self.referrer_reward_amount > 0:
                referrer_wallet = self.referrer.wallet
                referrer_wallet.credit(self.customer_reward_amount, self.order.number)
            
            self.status = 'CONFIRMED'
            self.save()

    def cancel_reward(self):
        """Cancel the reward in case of order cancellation"""
        if self.status != 'PENDING':
            print(f"Cannot cancel reward for order {self.order.number} as it is not pending and cancelled.")
            return
        
        with transaction.atomic():
            if self.customer_reward_amount > 0:
                customer_wallet = self.order.user.wallet
                customer_wallet.debit(self.order.number)
            
            if self.referrer and self.referrer_reward_amount > 0:
                referrer_wallet = self.referrer.wallet
                referrer_wallet.debit(self.order.number)
        
            self.status = 'CANCELLED'
            self.save()

    def __str__(self):
        return f"{self.status} Pending reward for order {self.order.number} - Customer: ${self.customer_reward_amount}, Referrer: ${self.referrer_reward_amount}"