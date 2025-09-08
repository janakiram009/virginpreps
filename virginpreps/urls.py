from django.apps import apps
from django.urls import include, path
from django.contrib import admin
from django.shortcuts import render
from apps.customer import urls as customer_urls

# from django_otp.admin import AdminSite, OTPAdmin

# OTPAdmin.enable()
# admin.site = AdminSite()


def grocee(request):
    return render(request, "oscar/grocee.html")


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("accounts/", include(customer_urls)),
    path("rewards/", include("rewards.urls")),
    path("oscar/", include(apps.get_app_config("oscar").urls[0])),
    # path("grocee/", grocee, name="grocee"),
    path("", grocee, name="grocee"),
]

from django.conf import settings

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static

    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + debug_toolbar_urls()
    )
