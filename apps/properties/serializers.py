from rest_framework import serializers
from .models import Property, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'description']


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    embed_src = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['public_id', 'name', 'type', 'description', 'list_details', 'summary', 'location', 'map_embed_url', 'embed_src', 'created_at', 'images']

    def get_embed_src(self, obj):
        return obj.embed_src
