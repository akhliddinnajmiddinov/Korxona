from rest_framework import serializers

class RequestSerializer(serializers.Serializer):
    order = serializers.ListField(child=serializers.DictField())

class ProductQuantitySerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=100)
    product_qty = serializers.IntegerField()
    
    class Meta:
        fields = ['product_name', 'product_qty']