# offer/benefits.py - Custom benefits for wallet rewards

from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from oscar.apps.offer.benefits import Benefit
from oscar.apps.offer.models import Benefit as BenefitModel
from oscar.core.loading import get_model

# Import your wallet models
from .models import WalletRewardConfiguration, PendingWalletReward

class WalletRewardBenefit(Benefit):
    """
    Custom benefit that creates pending wallet rewards instead of applying discounts
    """
    name = _("Wallet Reward")
    description = _("Credit wallet with percentage of order value")

    def apply(self, basket, condition, offer, **kwargs):
        """
        This method is called during basket processing but we don't apply immediate discounts.
        Instead, we store information for later processing after payment.
        """
        # Return zero discount since we're not applying immediate discounts
        return Decimal('0.00')

    def calculate_wallet_reward(self, order_total, config=None):
        """
        Calculate wallet reward amounts based on configuration
        """
        if not config:
            config = WalletRewardConfiguration.get_active_config()
        
        if not config or order_total < config.minimum_order_value:
            return Decimal('0.00'), Decimal('0.00')
        
        customer_reward = (order_total * config.customer_reward_percentage) / 100
        referrer_reward = (order_total * config.referrer_reward_percentage) / 100
        
        return customer_reward, referrer_reward

    def can_apply_benefit(self, line, stockrecord=None, user=None):
        """
        Determine if this benefit can be applied to a basket line
        """
        # Always return True as we handle eligibility at order level
        return True

    def apply_benefit(self, basket, **kwargs):
        """
        Apply the benefit to the basket (called by Oscar's offer system)
        """
        # We don't apply immediate discounts, so return zero
        return Decimal('0.00')

    @property
    def benefit_class_type(self):
        return "wallet_reward"


class ReferralWalletRewardBenefit(WalletRewardBenefit):
    """
    Specific benefit for referral rewards
    """
    name = _("Referral Wallet Reward")
    description = _("Credit referrer's wallet with percentage of order value")

    def can_apply_benefit(self, line, stockrecord=None, user=None):
        """
        Only apply if user has a referrer
        """
        if not user or not hasattr(user, 'referred_by'):
            return False
        return user.referred_by is not None


# Custom benefit model to store in database
class WalletRewardBenefitModel(BenefitModel):
    """
    Custom benefit model that stores wallet reward configuration
    """
    class Meta:
        proxy = True
        verbose_name = _("Wallet Reward Benefit")
        verbose_name_plural = _("Wallet Reward Benefits")

    def benefit_class(self):
        return WalletRewardBenefit

    def description(self):
        return _("Wallet reward benefit")


# Register the benefit classes
from oscar.apps.offer.benefits import BENEFIT_CLASSES
BENEFIT_CLASSES['wallet_reward'] = WalletRewardBenefit
BENEFIT_CLASSES['referral_wallet_reward'] = ReferralWalletRewardBenefit