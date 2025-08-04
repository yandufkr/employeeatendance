import os
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('faceatendance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'faceatendance', 'static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
