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


def subscription(request):
    return render(request, "oscar/catalogue/sub-form.html")


def veggiesestimation(request):
    return render(request, "oscar/veggiesestimation.html")


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("accounts/", include((customer_urls))),
    path("rewards/", include(("rewards.urls", "rewards"))),
    path("", include(apps.get_app_config("oscar").urls[0])),
    path("grocee/", grocee, name="grocee"),
    path("subscription/", subscription, name="subscription"),
    path("veggiesestimation/", veggiesestimation, name="veggiesestimation"),
]

# from . import views

# urlpatterns += [
#     path("vegetables/", views.VegetableListView.as_view(), name="vegetable_list"),
#     path("vegetables/add/", views.VegetableCreateView.as_view(), name="vegetable_add"),
#     path(
#         "vegetables/<int:pk>/update/",
#         views.VegetableUpdateView.as_view(),
#         name="vegetable_update",
#     ),
#     path("customers/", views.CustomerListView.as_view(), name="customer_list"),
#     path("customers/add/", views.CustomerCreateView.as_view(), name="customer_add"),
#     path(
#         "customers/<int:pk>/update/",
#         views.CustomerUpdateView.as_view(),
#         name="customer_update",
#     ),
#     path(
#         "customers/<int:pk>/blacklist/",
#         views.BlacklistUpdateView.as_view(),
#         name="blacklist_update",
#     ),
# ]


from django.conf import settings

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    from django.conf.urls.static import static

    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + debug_toolbar_urls()
    )
