from oscar.apps.checkout import forms as checkout_forms

class GatewayForm(checkout_forms.GatewayForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email field optional
        if 'email' in self.fields:
            self.fields['email'].required = False

# class GuestForm(checkout_forms.GuestForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Make email field optional
#         self.fields['email'].required = False