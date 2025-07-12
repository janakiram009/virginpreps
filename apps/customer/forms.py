
from django import forms

class PhoneOTPForm(forms.Form):
    phone = forms.CharField(max_length=15)
    otp = forms.CharField(max_length=6, required=False)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Add basic validation here or use a regex/PhoneNumberField
        return phone

# from oscar.apps.customer.forms import ProfileForm as CoreProfileForm
# from oscar.core.compat import existing_user_fields
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ProfileForm(CoreProfileForm):
#     class Meta(CoreProfileForm.Meta):
#         model = User
#         fields = existing_user_fields(['first_name', 'last_name', 'email', 'nickname', 'bio'])
