"""
This module contains serializers for the various models in the application.
"""

from rest_framework import serializers
from .models import (
    Brand,
    GroupProduct,
    Feature,
    Product,
    FeatureValue,
    ProductFeature,
    ProductGallery
)


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for the Brand model."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = Brand
        fields = '__all__'  # pylint: disable=missing-class-docstring


class GroupProductSerializer(serializers.ModelSerializer):
    """Serializer for the GroupProduct model."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = GroupProduct
        fields = '__all__'  # pylint: disable=missing-class-docstring


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for the Feature model."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = Feature
        fields = '__all__'  # pylint: disable=missing-class-docstring


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = Product
        fields = '__all__'  # pylint: disable=missing-class-docstring


class ProductFeatureSerializer(serializers.ModelSerializer):
    """Serializer for the ProductFeature model."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = ProductFeature
        fields = '__all__'  # pylint: disable=missing-class-docstring


class FeatureValueSerializer(serializers.ModelSerializer):
    """Serializer for the FeatureValue model."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = FeatureValue
        fields = '__all__'  # pylint: disable=missing-class-docstring


class ProductGallerySerializer(serializers.ModelSerializer):
    """Serializer for the ProductGallery model."""

    class Meta:  # pylint: disable=missing-class-docstring
        model = ProductGallery
        fields = '__all__'  # pylint: disable=missing-class-docstring
