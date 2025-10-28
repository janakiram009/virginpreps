from django import forms
from .models import Vegetable, Customer


class VegetableForm(forms.ModelForm):
    class Meta:
        model = Vegetable
        fields = ["name", "price"]  # Inputs: name and current market price
        widgets = {
            "price": forms.NumberInput(attrs={"step": "0.01"}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name"]  # Input: customer name (add more fields as needed)


class BlacklistForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["blacklisted_vegetables"]
        widgets = {
            "blacklisted_vegetables": forms.CheckboxSelectMultiple(),
        }
