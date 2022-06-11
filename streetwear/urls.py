"""streetwear URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from products.views import ProductModelViewSet, CategoryModelListApiView, SizeModelListApiView, ColorModelListApiView

schema_view = get_schema_view(openapi.Info(
    title="StreetWear",
    default_version='1.0',
    description="Documentation for StreetWear API",
    contact=openapi.Contact(email="admin@admin.local"),
    license=openapi.License(name="MIT License"), ),
    public=True, permission_classes=(AllowAny,), )

router = DefaultRouter()
router.register('products', ProductModelViewSet)
router.register('categories', CategoryModelListApiView)
router.register('colors', ColorModelListApiView)
router.register('sizes', SizeModelListApiView)

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
