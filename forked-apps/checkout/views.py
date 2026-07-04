from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from oscar.apps.checkout.views import PaymentDetailsView as CorePaymentDetailsView
from oscar.apps.payment import models
from oscar.apps.payment.exceptions import UnableToTakePayment

from payments.models import RazorpayPayment
from payments.services import create_razorpay_order, verify_payment


class PaymentDetailsView(CorePaymentDetailsView):
    template_name = "oscar/checkout/payment_details.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        order_number = self.generate_order_number(self.request.basket)
        total = ctx.get("order_total")

        if total is None:
            total = self.build_submission(basket=self.request.basket)["order_total"]

        rp_order = create_razorpay_order(order_number, total.incl_tax)

        RazorpayPayment.objects.get_or_create(
            razorpay_order_id=rp_order["id"],
            defaults={
                "basket_id": self.request.basket.id,
                "amount": total.incl_tax,
            },
        )

        ctx["razorpay_key"] = settings.RAZORPAY_KEY_ID
        ctx["razorpay_order_id"] = rp_order["id"]
        ctx["razorpay_amount"] = rp_order["amount"]
        return ctx

    def handle_payment(self, order_number, total, **kwargs):
        payment = RazorpayPayment.objects.filter(
            basket_id=self.request.basket.id,
            status="captured",
        ).last()

        if not payment:
            raise UnableToTakePayment("Payment not completed")

        source_type, _ = models.SourceType.objects.get_or_create(name="Razorpay")
        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            amount_debited=total.incl_tax,
            reference=payment.razorpay_payment_id,
        )

        self.add_payment_source(source)
        self.add_payment_event("Paid", total.incl_tax)


class RazorpayCallbackView(View):
    def get(self, request):
        return self.handle_callback(request)

    def post(self, request):
        return self.handle_callback(request)

    def handle_callback(self, request):
        payment_id = request.POST.get("razorpay_payment_id") or request.GET.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id") or request.GET.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature") or request.GET.get("razorpay_signature")

        if not all([payment_id, order_id, signature]):
            messages.error(request, "Payment data missing. Please try again.")
            return redirect("checkout:payment-details")

        try:
            verify_payment(payment_id, order_id, signature)
        except Exception:
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect("checkout:payment-details")

        payment = RazorpayPayment.objects.get(razorpay_order_id=order_id)
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = "captured"
        payment.save()

        messages.success(request, "Payment successful. Redirecting to order preview...")
        return redirect("checkout:preview")