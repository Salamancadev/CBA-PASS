from rest_framework import serializers
from .models import Usuario, QR, HistorialAcceso

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class QRSerializer(serializers.ModelSerializer):
    class Meta:
        model = QR
        fields = '__all__'

class HistorialAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialAcceso
        fields = '__all__'