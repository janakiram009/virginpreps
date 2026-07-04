from django.db import models
from oscar.apps.order.models import Order


class RazorpayPayment(models.Model):
    order = models.ForeignKey(
        Order,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    basket_id = models.IntegerField()

    razorpay_order_id = models.CharField(
        max_length=100,
        unique=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        default="created"
    )

    created = models.DateTimeField(
        auto_now_add=True
    )