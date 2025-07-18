from rest_framework import generics
from .models import Usuario, QR, HistorialAcceso
from .serializers import UsuarioSerializer, QRSerializer, HistorialAccesoSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario, QR
from rest_framework.serializers import ModelSerializer
import uuid
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from .models import HistorialAcceso

    
# Usuario
class UsuarioListCreate(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# QR
class QRListCreate(generics.ListCreateAPIView):
    queryset = QR.objects.all()
    serializer_class = QRSerializer

class QRRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = QR.objects.all()
    serializer_class = QRSerializer

# Historial
class HistorialListCreate(generics.ListCreateAPIView):
    queryset = HistorialAcceso.objects.all()
    serializer_class = HistorialAccesoSerializer

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

        # Crear el usuario del sistema
        user = User.objects.create_user(username=username, password=password)

        # Crear el modelo personalizado
        usuario = Usuario.objects.create(
            user=user,
            nombres=nombres,
            apellidos=apellidos,
            tipo=tipo,
            documento=documento,
            email=email
        )

        # Generar un código QR único
        codigo_qr = str(uuid.uuid4())
        QR.objects.create(usuario=usuario, codigo=codigo_qr)

        return Response({"mensaje": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)
    
class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

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
            # Validaciones de duplicados
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

            # Actualiza también el modelo User
            if nuevo_username:
                user.username = nuevo_username
            if nuevo_email:
                user.email = nuevo_email
            user.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=400)
        
class GenerarQRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user.perfil
        if hasattr(usuario, 'qr'):
            return Response({'detalle': 'QR ya generado.'}, status=400)

        codigo_qr = get_random_string(20)  # Generar un código aleatorio
        qr = QR.objects.create(usuario=usuario, codigo=codigo_qr)
        return Response({'mensaje': 'QR generado', 'codigo': qr.codigo})

class RegistrarAccesoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tipo_evento = request.data.get('tipo')  # 'entrada' o 'salida'
        if tipo_evento not in ['entrada', 'salida']:
            return Response({'error': 'Tipo de evento inválido'}, status=400)

        usuario = request.user.perfil
        HistorialAcceso.objects.create(usuario=usuario, tipo_evento=tipo_evento)
        return Response({'mensaje': f'{tipo_evento.capitalize()} registrada'})
    
class ActualizarPerfilAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        usuario = request.user.perfil # Asegúrate de que esto sea correcto
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
