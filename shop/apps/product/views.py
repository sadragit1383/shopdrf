"""
Views for handling brand, group product, feature, product, feature value,
product feature, and product gallery API endpoints.
"""

from rest_framework import generics
from .models import (
    Brand,
    GroupProduct,
    Feature,
    Product,
    FeatureValue,
    ProductFeature,
    ProductGallery
)

from .serializers import (
    BrandSerializer,
    GroupProductSerializer,
    FeatureSerializer,
    ProductSerializer,
    FeatureValueSerializer,
    ProductFeatureSerializer,
    ProductGallerySerializer
)
# Brand views
class BrandGenericProduct(generics.ListCreateAPIView):
    """Handles listing and creating Brand instances."""
    queryset = Brand.objects.all().order_by('register_date')
    serializer_class = BrandSerializer


class BrandGenericProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a Brand instance."""
    queryset = Brand.objects.all().order_by('register_date')
    serializer_class = BrandSerializer


# Group Product views
class GroupProductGeneric(generics.ListCreateAPIView):
    """Handles listing and creating GroupProduct instances."""
    queryset = GroupProduct.objects.all().order_by('register_date')
    serializer_class = GroupProductSerializer


class GroupProductGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a GroupProduct instance."""
    queryset = GroupProduct.objects.all().order_by('register_date')
    serializer_class = GroupProductSerializer


# Feature views
class FeatureGeneric(generics.ListCreateAPIView):
    """Handles listing and creating Feature instances."""
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class FeatureGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a Feature instance."""
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


# Product views
class ProductGeneric(generics.ListCreateAPIView):
    """Handles listing and creating Product instances."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a Product instance."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Feature Value views
class FeatureValueGeneric(generics.ListCreateAPIView):
    """Handles listing and creating FeatureValue instances."""
    queryset = FeatureValue.objects.all()
    serializer_class = FeatureValueSerializer


class FeatureValueGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a FeatureValue instance."""
    queryset = FeatureValue.objects.all()
    serializer_class = FeatureValueSerializer


# Product Feature views
class ProductFeatureGeneric(generics.ListCreateAPIView):
    """Handles listing and creating ProductFeature instances."""
    queryset = ProductFeature.objects.all()
    serializer_class = ProductFeatureSerializer


class ProductFeatureGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a ProductFeature instance."""
    queryset = ProductFeature.objects.all()
    serializer_class = ProductFeatureSerializer


# Product Gallery views
class ProductGalleryGeneric(generics.ListCreateAPIView):
    """Handles listing and creating ProductGallery instances."""
    queryset = ProductGallery.objects.all()
    serializer_class = ProductGallerySerializer


class ProductGalleryGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a ProductGallery instance."""
    queryset = ProductGallery.objects.all()
    serializer_class = ProductGallerySerializer


class CheapestProductGeneric(generics.ListAPIView):

    serializer_class = ProductSerializer


    def get_queryset(self):
        products = Product.objects.filter(is_active = True).order_by('-price')
        return products

class ProductRecentllyGeneric(generics.ListAPIView):

    serializer_class = ProductSerializer




    def get_queryset(self):

        products = Product.objects.all().order_by('-register_date')

        return products


class DetailProductView(generics.ListAPIView):

    serializer_class = ProductSerializer


    def get(self, request, *args, **kwargs):

        pk = request.get.data('pk')
        product = Product.objects.filter(id = pk).first()

        return product



