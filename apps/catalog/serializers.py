from rest_framework import serializers

from apps.catalog.models import ProductAttributes, ProductImages, Product


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'value']
        model = ProductAttributes


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'mode', 'url']
        model = ProductImages


class ProductOptionSerializer(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True, read_only=True)
    product_attributes = ProductAttributesSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'price', 'product_attributes', 'product_images']
        model = ProductImages


class ProductSerializer(serializers.ModelSerializer):
    product_options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'name', 'description', 'sku_code', 'product_options', 'category']
        model = Product
        depth = 1
