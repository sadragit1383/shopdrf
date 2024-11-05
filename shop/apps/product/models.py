"""
This module defines the Brand model for representing brand information in the application.
"""
from django.utils import timezone
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import funcs # pylint: disable=import-error

class Brand(models.Model):
    """
    A model representing a Brand with details like name, slug, and image.
    """

    brand_name = models.CharField(max_length=200, verbose_name='Brand name')
    slug = models.CharField(max_length=100, verbose_name='slug url')
    image_file = funcs.FileUpload('images', 'brand_file')
    image_name = models.ImageField(upload_to=image_file.upload_to, verbose_name='brand image')
    register_date = models.DateTimeField(verbose_name='Confirm time!', default=timezone.now)
    update_date = models.DateTimeField(auto_now=True, verbose_name='update time')
    is_active = models.BooleanField(default=True,verbose_name='status of brand')

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        """
        Metadata for the Brand model.
        """
        # pylint: disable=too-few-public-methods
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'



class GroupProduct(models.Model):
    """
    A model representing a group of products.
    """

    group_name = models.CharField(max_length=50,verbose_name='Group Name')
    file_upload = funcs.FileUpload('images','group_image')
    image_name = models.ImageField(verbose_name='image of group',upload_to=file_upload.upload_to)
    slug = models.CharField(max_length=100,verbose_name='slug url')
    register_date = models.DateTimeField(verbose_name='Confirm time!', default=timezone.now)
    update_date = models.DateTimeField(auto_now=True, verbose_name='update time')
    is_active = models.BooleanField(default=True,verbose_name='status of brand')
    group_parent = models.ForeignKey('GroupProduct',on_delete=models.CASCADE,verbose_name='Parent',
    related_name='Parent_of_product')

    def __str__(self):
        return str(self.group_name)

    class Meta:
        """
        Metadata for the Group product model.
        """
        # pylint: disable=too-few-public-methods
        verbose_name = 'group'
        verbose_name_plural = 'groups'


class Feature(models.Model):
    """
    A model representing a Feature of products.
    """

    feature_name = models.CharField(max_length=100,verbose_name='Feature name')
    product_group = models.ForeignKey(GroupProduct,on_delete=models.CASCADE,
    verbose_name='group feature',
    related_name='group_of_feature')

    def __str__(self) -> str:
        return str(self.feature_name)

    class Meta:
        """
        Metadata for the Group product model.
        """
        # pylint: disable=too-few-public-methods
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'


class Product(models.Model):
    """
    A model representing a Product with details like product_name, description, and image.
    """

    product_name = models.CharField(max_length=100,verbose_name='Product name')
    description = RichTextUploadingField(verbose_name='description',
    config_name = 'special',blank=True)
    file_upload = funcs.FileUpload('images','product')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name='image of product')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,
    related_name='brands')
    product_group=models.ManyToManyField(GroupProduct,verbose_name='group product',
    related_name='product_of_groups')
    price_buy = models.PositiveIntegerField(verbose_name='buy price',default=0)
    price = models.PositiveIntegerField(verbose_name='price',default=0)
    is_active = models.BooleanField(default=True,verbose_name='status')
    register_date = models.DateTimeField(verbose_name='Confirm time!', default=timezone.now)
    update_date = models.DateTimeField(auto_now=True, verbose_name='update time')
    features = models.ManyToManyField(Feature,through='ProductFeature')
    slug = models.CharField(max_length=30,verbose_name='اسلاگ',blank=True,null=True)


    def __str__(self):
        return str(self.product_name)


    class Meta:
        """
        Metadata for the  product model.
        """
        # pylint: disable=too-few-public-methods
        verbose_name = 'product'
        verbose_name_plural = 'products'


class FeatureValue(models.Model):
    """
    A model representing a FeatureValue with details like value_title, feature, and english_value.
    """

    value_title = models.CharField(max_length=100,verbose_name='title')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,
    verbose_name='feature',null=True,blank=True,related_name='feature_value')
    english_value = models.CharField(max_length=20,verbose_name='feature',null=True,blank=True)


    def __str__(self):
        return str(self.value_title)

    class Meta:
        """
        Metadata for the  FeatureValue model.
        """
        verbose_name = 'Feature value'
        verbose_name_plural = 'Feature Values'


class ProductFeature(models.Model):
    """
    A model representing a ProductFeature with details like product, product, and value.
    """
    product = models.ForeignKey(Product,on_delete=models.CASCADE,
    verbose_name='product',related_name='features_value')
    feature = models.ForeignKey(Feature,verbose_name='feature',
    on_delete=models.CASCADE,related_name='feature_product')
    value = models.CharField(max_length=40,verbose_name='value feature')
    english = models.CharField(verbose_name='english',max_length=20,blank=True,null=True)
    filter_value = models.ForeignKey(FeatureValue,null=True,blank=True,
    on_delete=models.CASCADE,verbose_name='filtring value')


    def __str__(self) -> str:
        return str(self.value)


    class Meta:
        """
        Metadata for the  ProductFeature model.
        """
        verbose_name = 'Product Feature'
        verbose_name_plural = 'Product Featues'


class ProductGallery(models.Model):
    """
    A model representing a ProductFeature with details like product, product, and value.
    """
    product = models.ForeignKey(Product,on_delete=models.CASCADE,
    verbose_name='product',related_name='Product_Gallery')
    file_upload = funcs.FileUpload('images','product_gallery_img')
    image_name = models.ImageField(upload_to=file_upload.upload_to,verbose_name='images')


    class Meta:
        """
        Metadata for the  ProductFeature model.
        """
        verbose_name = 'Image'
        verbose_name_plural = 'Images'