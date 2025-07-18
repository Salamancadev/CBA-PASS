from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.serializers import ModelSerializer
from .models import Usuario, QR, HistorialAcceso
from .serializers import UsuarioSerializer, QRSerializer, HistorialAccesoSerializer
import uuid
from rest_framework.permissions import IsAuthenticated

# ---------------------- VISTAS BASADAS EN CLASES --------------------------

class UsuarioListCreate(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class QRListCreate(generics.ListCreateAPIView):
    queryset = QR.objects.all()
    serializer_class = QRSerializer

class QRRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = QR.objects.all()
    serializer_class = QRSerializer

class HistorialListCreate(generics.ListCreateAPIView):
    serializer_class = HistorialAccesoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Asegura que accedes al perfil relacionado con el user
        return HistorialAcceso.objects.filter(usuario=self.request.user.perfil)

class HistorialRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistorialAcceso.objects.all()
    serializer_class = HistorialAccesoSerializer

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        nombres = request.data.get("nombres")
        apellidos = request.data.get("apellidos")
        tipo = request.data.get("tipo")
        documento = request.data.get("documento")
        email = request.data.get("email", "")

        if User.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        usuario = Usuario.objects.create(
            user=user,
            nombres=nombres,
            apellidos=apellidos,
            tipo=tipo,
            documento=documento,
            email=email
        )

        QR.objects.create(usuario=usuario, codigo=str(uuid.uuid4()))
        return Response({"mensaje": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)

class PerfilUsuarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            perfil = Usuario.objects.get(user=request.user)
            serializer = UsuarioSerializer(perfil)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response({'error': 'Perfil no encontrado'}, status=404)

    def put(self, request):
        try:
            perfil = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            return Response({'error': 'Perfil no encontrado'}, status=404)

        serializer = UsuarioSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            nuevo_username = request.data.get('username')
            nuevo_email = request.data.get('email')
            user = request.user

            if nuevo_username and nuevo_username != user.username:
                if User.objects.filter(username=nuevo_username).exclude(pk=user.pk).exists():
                    return Response({'error': 'El nombre de usuario ya está en uso.'}, status=400)

            if nuevo_email and nuevo_email != user.email:
                if User.objects.filter(email=nuevo_email).exclude(pk=user.pk).exists():
                    return Response({'error': 'El correo electrónico ya está en uso.'}, status=400)

            serializer.save()
            if nuevo_username:
                user.username = nuevo_username
            if nuevo_email:
                user.email = nuevo_email
            user.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)

class GenerarQRView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        usuario = request.user.perfil
        if hasattr(usuario, 'qr'):
            return Response({'detalle': 'QR ya generado.'}, status=400)

        codigo_qr = get_random_string(20)
        qr = QR.objects.create(usuario=usuario, codigo=codigo_qr)
        return Response({'mensaje': 'QR generado', 'codigo': qr.codigo})

class ActualizarPerfilAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        usuario = request.user.perfil
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class HistorialAccesoListView(generics.ListAPIView):
    serializer_class = HistorialAccesoSerializer

    def get_queryset(self):
        return HistorialAcceso.objects.filter(usuario=self.request.user)
    
class HistorialAccesoCreateView(generics.CreateAPIView):
    serializer_class = HistorialAccesoSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class RegistrarAccesoView(APIView):
    serializer_class = HistorialAccesoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            usuario = Usuario.objects.get(user=request.user)
            HistorialAcceso.objects.create(usuario=usuario, accion='entrada')  # asegurate de que sea 'accion'
            return Response({'mensaje': 'Acceso registrado'}, status=status.HTTP_201_CREATED)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_queryset(self):
        return HistorialAcceso.objects.filter(usuario=self.request.user)
    
    