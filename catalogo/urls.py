from django.urls import path, include
from catalogo.views import (
    LibroListCreate, LibroRetrieveUpdateDelete,
)
from rest_framework.routers import DefaultRouter
from catalogo.views import LibroViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'libros', LibroViewSet)  # /libros/ , /libros/{id}/

urlpatterns = [
    # JWT Auth endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Estilo APIView
    path('apiview/libros/', LibroListCreate.as_view()),
    path('apiview/libros/<int:pk>/', LibroRetrieveUpdateDelete.as_view()),

    # ...existing code...

    # Estilo ViewSet + Router
    path('', include(router.urls)),
]
