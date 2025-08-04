from django.urls import path
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import register_employee, capture_page, recognize, redirect_to_capture

urlpatterns = [
    path('register/', register_employee, name='register_employee'),
    path('capture/', capture_page, name='capture'),
    path('recognize/', recognize, name='recognize'),
    path('redirect/', redirect_to_capture, name='redirect'),

    # Redirect root URL to register page
    path('', RedirectView.as_view(pattern_name='register_employee', permanent=False)),
]
