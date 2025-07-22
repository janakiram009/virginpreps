from django.apps import apps
from django.urls import include, path
from django.contrib import admin
from apps.customer import urls as customer_urls

# from django_otp.admin import AdminSite, OTPAdmin

# OTPAdmin.enable()
# admin.site = AdminSite()



urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),

    path('admin/', admin.site.urls),

    path('accounts/', include(customer_urls)),
    path('rewards/', include('rewards.urls')),
    path('', include(apps.get_app_config('oscar').urls[0])),

    # path(r'qr/', include("django_otp.urls")),
]

from django.conf import settings

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()

