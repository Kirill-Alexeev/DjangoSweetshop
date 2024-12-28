from rest_framework import serializers
from .models import Cake, Order


class CakeSerializer(serializers.ModelSerializer):
    ingredients = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cake
        fields = [
            "id",
            "title",
            "weight",
            "description",
            "image",
            "price",
            "ingredients",
            "created_at",
            "updated_at",
        ]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    cakes = serializers.StringRelatedField(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "execution_date",
            "status",
            "cost",
            "cakes",
            "delivery_address",
            "created_at",
            "updated_at",
        ]
