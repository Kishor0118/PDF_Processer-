from rest_framework import serializers
from .models import ExtractedData

class ExtractedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedData
        fields = ['email', 'nouns', 'verbs']
