from django.urls import path
from .views import (
    BrandGenericProduct,
    BrandGenericProductDetail,
    GroupProductGeneric,
    GroupProductGenericDetail,
    FeatureGeneric,
    FeatureGenericDetail,
    ProductGeneric,
    ProductGenericDetail,
    FeatureValueGeneric,
    FeatureValueGenericDetail,
    ProductFeatureGeneric,
    ProductFeatureGenericDetail,
    ProductGalleryGeneric,
    ProductGalleryGenericDetail,
)

urlpatterns = [
    # Brand URLs
    path('brands/', BrandGenericProduct.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', BrandGenericProductDetail.as_view(), name='brand-detail'),

    # GroupProduct URLs
    path('group-products/', GroupProductGeneric.as_view(), name='group-product-list-create'),
    path('group-products/<int:pk>/', GroupProductGenericDetail.as_view(), name='group-product-detail'),

    # Feature URLs
    path('features/', FeatureGeneric.as_view(), name='feature-list-create'),
    path('features/<int:pk>/', FeatureGenericDetail.as_view(), name='feature-detail'),

    # Product URLs
    path('products/', ProductGeneric.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductGenericDetail.as_view(), name='product-detail'),

    # FeatureValue URLs
    path('feature-values/', FeatureValueGeneric.as_view(), name='feature-value-list-create'),
    path('feature-values/<int:pk>/', FeatureValueGenericDetail.as_view(), name='feature-value-detail'),

    # ProductFeature URLs
    path('product-features/', ProductFeatureGeneric.as_view(), name='product-feature-list-create'),
    path('product-features/<int:pk>/', ProductFeatureGenericDetail.as_view(), name='product-feature-detail'),

    # ProductGallery URLs
    path('product-galleries/', ProductGalleryGeneric.as_view(), name='product-gallery-list-create'),
    path('product-galleries/<int:pk>/', ProductGalleryGenericDetail.as_view(), name='product-gallery-detail'),
]
