from rest_framework import serializers
from .models import Usuario, QR, HistorialAcceso

class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Usuario
        fields = '__all__'

    def update(self, instance, validated_data):
        # Extraer los datos del modelo User
        user_data = validated_data.pop('user', {})

        # Actualizar campos del modelo Usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Actualizar campos del modelo User
        user = instance.user
        username = user_data.get('username')
        if username:
            user.username = username
            user.save()

        return instance

class QRSerializer(serializers.ModelSerializer):
    class Meta:
        model = QR
        fields = '__all__'

class HistorialAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialAcceso
        fields = '__all__'