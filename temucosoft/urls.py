from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core.views import home, signup

schema_view = get_schema_view(
    openapi.Info(
        title="API Gestión de Transporte",
        default_version="v1",
        description="API para gestionar rutas, buses, conductores y viajes programados.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", home, name="home"),

    path("admin/", admin.site.urls),

    path("accounts/signup/", signup, name="signup"),

    # login, logout, password reset, etc.
    path("accounts/", include("django.contrib.auth.urls")),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API principal
    path("api/", include("core.urls")),

    # Swagger / Redoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
