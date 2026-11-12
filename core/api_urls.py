
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .api_views import PacoteViewSet, ReservaViewSet

router = DefaultRouter()
router.register("pacotes", PacoteViewSet, basename="api-pacote")
router.register("reservas", ReservaViewSet, basename="api-reserva")

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    path("", include(router.urls)),
]
