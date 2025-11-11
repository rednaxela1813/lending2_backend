from rest_framework import serializers
from orders.models import LegalAddressOrder


class LegalAddressOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalAddressOrder
        fields = [
            'public_id',
            'full_name',
            'email',
            'phone',
            'company_name',
            'address_choice',
            'note',
            'created_at',
        ]
        read_only_fields = ['public_id', 'created_at']
        
        
        
