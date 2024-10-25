
from rest_framework import routers, serializers, viewsets
from .models import Signup
# Serializers define the API representation.
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = '__all__'