import hmac
import hashlib
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def handle_payment_captured(payload):
    print("Payment captured event received:", payload)
    pass


def handle_payment_failed(payload):
    print("Payment failed event received:", payload)
    """Handle payment.failed event"""
    pass


def handle_refund(payload):
    """Handle refund.processed event"""
    print("Refund processed event received:", payload)
    pass


@csrf_exempt
def razorpay_webhook(request):

    if request.method != "POST":
        return HttpResponse(status=405)

    body = request.body

    received_signature = request.headers.get(
        "X-Razorpay-Signature"
    )

    generated_signature = hmac.new(
        bytes(settings.RAZORPAY_WEBHOOK_SECRET, 'utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(
        received_signature,
        generated_signature
    ):
        return HttpResponse(status=400)

    payload = json.loads(body)

    event = payload.get("event")

    if event == "payment.captured":
        handle_payment_captured(payload)

    elif event == "payment.failed":
        handle_payment_failed(payload)

    elif event == "refund.processed":
        handle_refund(payload)

    return HttpResponse(status=200)