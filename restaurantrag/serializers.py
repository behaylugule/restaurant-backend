# serializers.py
from rest_framework import serializers

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    k = serializers.IntegerField(required=False, default=6)
    use_conversational = serializers.BooleanField(required=False, default=False)
    conversation = serializers.ListField(child=serializers.DictField(), required=False)
