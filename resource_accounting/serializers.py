from rest_framework import serializers
from resource_accounting.models import Resource_accounting


class ResourceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource_accounting
        fields = '__all__'

