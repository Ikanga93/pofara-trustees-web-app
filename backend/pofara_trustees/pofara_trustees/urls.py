"""
URL configuration for pofara_trustees project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# API URL patterns
api_v1_patterns = [
    path('auth/', include('accounts.urls')),
    path('projects/', include('projects.urls')),
    path('inspectors/', include('inspectors.urls')),
    path('messaging/', include('messaging.urls')),
    path('payments/', include('payments.urls')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1
    path('api/v1/', include(api_v1_patterns)),
    
    # Health check endpoint (placeholder)
    # path('health/', include('django_extensions.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Custom error handlers (commented out for now)
# handler400 = 'pofara_trustees.views.bad_request'
# handler403 = 'pofara_trustees.views.permission_denied'
# handler404 = 'pofara_trustees.views.page_not_found'
# handler500 = 'pofara_trustees.views.server_error'
