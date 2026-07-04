from django.urls import path
import oscar.apps.checkout.apps as apps


class CheckoutConfig(apps.CheckoutConfig):
    name = 'forked-apps.checkout'

    def get_urls(self):
        from .views import RazorpayCallbackView

        urls = super().get_urls()
        urls += [
            path(
                "razorpay/callback/",
                RazorpayCallbackView.as_view(),
                name="razorpay-callback",
            ),
        ]
        return urls

