from rest_framework.views import APIView
from rest_framework.response import Response
# status: para respuestas HTTP, viewsets: para ViewSet, filters: búsqueda/orden
from rest_framework import status, viewsets, filters
# IsAuthenticated: protege las vistas con login/token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# DjangoFilterBackend: permite filtrar por campos
from django_filters.rest_framework import DjangoFilterBackend
from .models import Libro
# Importa el serializador para convertir modelos a JSON
from .serializers import LibroSerializer

# ViewSet para API REST con filtros, búsqueda y paginación
class LibroViewSet(viewsets.ModelViewSet):
    # Consulta todos los libros
    queryset = Libro.objects.all()
    # Usa el serializador para convertir a JSON
    serializer_class = LibroSerializer
    # Protege con autenticación
    permission_classes = [IsAuthenticated]
    # Permite filtrar, buscar y ordenar
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['autor', 'anio', 'titulo']  # filtro exacto por estos campos
    search_fields = ['titulo', 'autor', 'isbn']     # búsqueda por texto
    ordering_fields = ['anio', 'autor', 'titulo', 'creado']  # ordenar por estos campos
    ordering = ['creado']  # orden por defecto

class LibroListCreate(APIView):
    # Solo usuarios autenticados pueden acceder
    permission_classes = [IsAuthenticated]

    # GET: lista todos los libros
    def get(self, request):
        qs = Libro.objects.all()
        serializer = LibroSerializer(qs, many=True)
        return Response(serializer.data)

    # POST: crea un nuevo libro
    def post(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibroRetrieveUpdateDelete(APIView):
    # Solo usuarios autenticados pueden acceder
    permission_classes = [IsAuthenticated]

    # GET: obtiene un libro por su id (pk)
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return Response(LibroSerializer(libro).data)

    # PUT: actualiza todos los campos de un libro
    def put(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH: actualiza parcialmente un libro
    def patch(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: elimina un libro
    def delete(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

