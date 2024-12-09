# deploymate/ansible_api/serializers.py
from rest_framework import serializers

class ListToolsSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()

class InstallToolsSerializer(serializers.Serializer):
    host = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    tools = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        allow_empty=False
    )
