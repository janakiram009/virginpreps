import razorpay
from django.conf import settings


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET,
    )
)

def create_razorpay_order(
        order_number,
        amount
):
    return client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "receipt": str(order_number),
    })

def verify_payment(
        payment_id,
        order_id,
        signature
):
    client.utility.verify_payment_signature({
        "razorpay_payment_id": payment_id,
        "razorpay_order_id": order_id,
        "razorpay_signature": signature,
    })