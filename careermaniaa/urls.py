from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin', admin.site.urls),

    # for apps
    path('', include('mania.urls')),
    path('', include('merchant_app.urls')),

    # for password reset
    path('', include('django.contrib.auth.urls')),

    # for all-auth
    path('accounts/', include('allauth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # for any media, files
