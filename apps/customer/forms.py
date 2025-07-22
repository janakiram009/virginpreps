
from django import forms
from oscar.apps.customer.forms import UserForm as OscarUserForm
try:
    from oscar.apps.customer.forms import UserAndProfileForm as OscarUserAndProfileForm
except ImportError:
    OscarUserAndProfileForm = None  # Or define your own fallback here
from oscar.core.compat import existing_user_fields, get_user_model

User = get_user_model()

class UserForm(OscarUserForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "referred_by"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove 'referred_by' field if it already has a value
        if self.instance and self.instance.referred_by:
            self.fields.pop("referred_by", None)

if OscarUserAndProfileForm:
    class UserAndProfileForm(OscarUserAndProfileForm):
        pass
    ProfileForm = UserAndProfileForm
else:
    ProfileForm = UserForm

            
class PhoneOTPForm(forms.Form):
    phone = forms.CharField(max_length=15)
    otp = forms.CharField(max_length=6, required=False)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Add basic validation here or use a regex/PhoneNumberField
        return phone

# class UserForm(CoreUserForm):
#     class Meta(CoreUserForm.Meta):
#          fields = existing_user_fields(["first_name", "last_name", "email", "referred_by"])

# from oscar.apps.customer.forms import ProfileForm as CoreProfileForm
# from oscar.core.compat import existing_user_fields
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ProfileForm(CoreProfileForm):
#     class Meta(CoreProfileForm.Meta):
#         model = User
#         fields = existing_user_fields(['first_name', 'last_name', 'email', 'nickname', 'bio'])