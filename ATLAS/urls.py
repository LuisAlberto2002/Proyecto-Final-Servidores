"""
URL configuration for ATLAS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Atlas_app import views as atlas_views
from Atlas_app.views import (
    ClientsViewSet,
    CarsViewSet,
    ServiciosViewSet,
    ServiceOrdersViewSet,
    FacturesViewSet,
)
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)

router = DefaultRouter()
router.register(r'clients', ClientsViewSet)
router.register(r'cars', CarsViewSet)
router.register(r'servicios', ServiciosViewSet)
router.register(r'service-orders', ServiceOrdersViewSet)
router.register(r'factures', FacturesViewSet)

urlpatterns = [

    path("api/", include(router.urls)),
     path("", atlas_views.index,name='index'),
    path("cars/", atlas_views.cars_list, name="cars_list"),
    path("cars/create/", atlas_views.cars_create, name="cars_create"),
    path("cars/<int:pk>/edit/", atlas_views.cars_edit, name="cars_edit"),
    path("cars/<int:pk>/delete/", atlas_views.cars_delete, name="cars_delete"),

    path('admin/', admin.site.urls),
    path('api/', include('Atlas_app.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('', include('Atlas_app.web_urls')), # No queria modificar las rutas que mis companeros ya tenian hechas
]
