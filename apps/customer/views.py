from django.views.generic import FormView
from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib import messages
from .forms import PhoneOTPForm, ProfileForm
from .utils import send_sms_via_fast2sms
import random
from django.shortcuts import render
from django.contrib.auth import login, get_user_model

User = get_user_model()

class OTPLoginView(FormView):
    template_name = 'oscar/customer/login.html'
    form_class = PhoneOTPForm
    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        otp = form.cleaned_data.get('otp')
        print('entered form valid')
        if 'resend' in self.request.POST:
            new_otp = str(random.randint(100000, 999999))
            cache.set(f'otp_{phone}', new_otp, timeout=300)
            send_sms_via_fast2sms(phone, new_otp)
            messages.info(self.request, f"New OTP sent to {phone}")
            return self.render_to_response(self.get_context_data(form=form))
            
        if not otp:
            generated = str(random.randint(100000, 999999))
            cache.set(f'otp_{phone}', generated, timeout=300)
            print('OTP: ',cache.get(f'otp_{phone}'))
            # send_sms_via_fast2sms(phone, generated)
            messages.info(self.request, f"OTP sent to {phone} is {generated}")
            # self.template_name = 'oscar/customer/verify_otp.html'
            return render(self.request, self.template_name , self.get_context_data(form=form, is_otp_sent=True))

        if cache.get(f'otp_{phone}') == otp:
            print('otp matched')
            user, _ = User.objects.get_or_create(phone=phone)
            login(self.request, user)
            return redirect('/')
        else:
            print('otp not matched')
            form.add_error('otp', 'Invalid OTP')
            return self.form_invalid(form)


from oscar.apps.customer.views import ProfileView as CoreProfileView
from oscar.apps.customer.views import ProfileUpdateView as CoreProfileUpdateView
from rewards.models import Wallet

class ProfileView(CoreProfileView):

    def get_profile_fields(self, user):
        field_data = super().get_profile_fields(user)
        
        try:
            wallet = Wallet.objects.get(user=user)
            field_data.extend([
                {
                    'name': 'Wallet Balance',
                    'value': wallet.balance,
                    'is_currency': True  # Custom flag for template
                }
            ])
        except Wallet.DoesNotExist:
            print("Wallet does not exist for user:", user)
            pass
            
        return field_data
    
    
class ProfileUpdateView(CoreProfileUpdateView):
    form_class = ProfileForm  # Use the custom UserForm defined in forms.py


from django.views import generic
class ReferredListView(generic.ListView):
    template_name = "oscar/customer/profile/referred.html"
    # context_object_name = "my_referred"
    def get_queryset(self):
        return User.objects.filter(referred_by=self.request.user)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the default context
        context = super().get_context_data(**kwargs)
        
        # Add your custom context data
        my_referred = self.get_queryset()
        context['page_title'] = 'Referred By Me'
        context['my_referred'] = my_referred
        context['count'] = my_referred.count()
        
        return context

