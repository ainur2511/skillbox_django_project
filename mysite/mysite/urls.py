
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from mysite.sitemaps import sitemaps

urlpatterns = []

urlpatterns += i18n_patterns(
    path('accounts/', include('myauth.urls')),
        path('blog/', include('blogapp.urls')),
        path('shop/', include('shopapp.urls')),
        path('admin/doc/', include('django.contrib.admindocs.urls')),
        path('admin/', admin.site.urls),
        path ('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    )

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
