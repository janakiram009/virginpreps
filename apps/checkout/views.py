from oscar.apps.checkout import views as checkout_views
from . import forms

class IndexView(checkout_views.IndexView):
    def get_form_class(self):
        if self.request.user.is_authenticated:
            return forms.GatewayForm
        return forms.GuestForm