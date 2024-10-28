from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from djangollmapi import views
from apis.views import (PermissionTestView, SingletonView,
                        ApiView, UsageApiView)

title = settings.PROJECT_NAME
admin.site.site_header = title
admin.site.site_title = title

urlpatterns = [
    path('', views.index, name='index'),
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('permission_test/', PermissionTestView.as_view(),
         name='permission_test'),
    path('singleton/<value>', SingletonView.as_view(), name='singleton'),
    path('analyze/', ApiView.as_view(), name='api'),
    path('usage/', UsageApiView.as_view(), name='api'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
