"""
URL configuration for InstrumentHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .views import add_instrument, delete_user, rent_instrument
# from notification import views
# from .views import ResetPasswordView


urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("", views.landing, name="landing"),
    path("about/", views.about_us, name="about_us"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path("live-listings", views.livelistings, name="livelistings"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("users/", views.users, name="users"),
    path("delete_user/<int:user_id>", views.delete_user, name="delete_user"),
    path("add_instrument/", add_instrument, name="add_instrument"),
    path(
        "change-password/<token>/<username>",
        views.changePassword,
        name="change_password",
    ),
    path("forget-password/", views.ForgetPassword, name="forget_password"),
    # path('password-reset/', ResetPasswordView.as_view(), name='forgot_password'),
    path("password_reset_done/", views.password_reset_done, name="password_reset_done"),
    path(
        "instrumet-update/<int:id>", views.instrument_update, name="update_instruments"
    ),
    path(
        "instrument-delete/<int:id>", views.instrument_delete, name="instrument_delete"
    ),
    path(
        "instrument-details/<int:id>",
        views.instrument_details,
        name="instrument_details",
    ),
    path("customer-dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path("my-listings/", views.my_listings, name="my_listings"),
    # path('search/', views.search_results, name='search_results'),
    path(
        "rent_instrument/<int:instrument_id>", rent_instrument, name="rent_instrument"
    ),
    path("instrument-reports/", views.instrument_reports, name="instrument_reports"),
    path("my-rentals/", views.my_rentals, name="my_rentals"),
    path(
        "return-instrument/<int:id>",
        views.return_instrument,
        name="return_instrument",
    ),
    # path("",views.notification_page_view, name="notification_page")
    path('', views.index, name = 'index'),
    path('upload', views.fileupload, name = "File_Uploads")
]
