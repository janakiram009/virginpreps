from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from .models import Vegetable, Customer
from .forms import VegetableForm, CustomerForm, BlacklistForm


class VegetableCreateView(CreateView):
    model = Vegetable
    form_class = VegetableForm
    template_name = "vegetable_delivery/vegetable_form.html"
    success_url = reverse_lazy("vegetable_list")


class VegetableUpdateView(UpdateView):  # For daily price updates
    model = Vegetable
    form_class = VegetableForm
    template_name = "vegetable_delivery/vegetable_form.html"
    success_url = reverse_lazy("vegetable_list")


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "vegetable_delivery/customer_form.html"
    success_url = reverse_lazy("customer_list")


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "vegetable_delivery/customer_form.html"
    success_url = reverse_lazy("customer_list")


class BlacklistUpdateView(UpdateView):
    model = Customer
    form_class = BlacklistForm
    template_name = "vegetable_delivery/blacklist_form.html"
    success_url = reverse_lazy("customer_list")

    def form_valid(self, form):
        form.save()  # Saves M2M blacklisted_vegetables
        return super().form_valid(form)


class VegetableListView(ListView):
    model = Vegetable
    template_name = "vegetable_delivery/vegetable_list.html"
    context_object_name = "vegetables"


class CustomerListView(ListView):
    model = Customer
    template_name = "vegetable_delivery/customer_list.html"
    context_object_name = "customers"
