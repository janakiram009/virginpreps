# your_project/apps/customer/urls.py

from django.urls import path
from .views import OTPLoginView, ReferredListView

urlpatterns = [
    path('login/', OTPLoginView.as_view(), name='login'),
    path('referred/', ReferredListView.as_view(), name='referred'),
    # path('register/', OTPLoginView.as_view(), name='register'),
    # you can also replace 'register/' with OTPLoginView
]
