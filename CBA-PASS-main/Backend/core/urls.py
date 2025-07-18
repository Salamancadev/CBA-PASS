from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import PerfilUsuarioView
from .views import GenerarQRView, RegistrarAccesoView


urlpatterns = [
    # Usuarios
    path('usuarios/', views.UsuarioListCreate.as_view(), name='usuarios-list-create'),
    path('usuarios/<int:pk>/', views.UsuarioRetrieveUpdateDestroy.as_view(), name='usuarios-detail'),

    # QR
    path('qrs/', views.QRListCreate.as_view(), name='qrs-list-create'),
    path('qrs/<int:pk>/', views.QRRetrieveUpdateDestroy.as_view(), name='qrs-detail'),

    # Historial
    path('historiales/', views.HistorialListCreate.as_view(), name='historial-list-create'),
    path('historiales/<int:pk>/', views.HistorialRetrieveUpdateDestroy.as_view(), name='historial-detail'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh

    # 🔐 Registro
    path('register/', views.RegisterView.as_view(), name='register'),
    # (Login ya lo tienes por defecto si usas /api/token/)

    path('perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),

    path('api/generar-qr/', GenerarQRView.as_view(), name='generar_qr'),
    path('registrar-acceso/', RegistrarAccesoView.as_view(), name='registrar_acceso'),

    path('perfil/actualizar/', views.ActualizarPerfilAPIView.as_view(), name='actualizar-perfil'),
    
]