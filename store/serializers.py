from decimal import Decimal
from store.models import Product, Collection, Likes
from rest_framework import serializers


class HyperlinkSerializer(serializers.Serializer):
    product = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='slug')
    collection = serializers.HyperlinkedIdentityField(view_name='collection-detail', lookup_field='slug')


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price", "customers_liked", "likes_count", "unit_price_tax", "collection"]

    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name="store:collection_details"
    )

    unit_price_tax = serializers.SerializerMethodField(
        method_name='tax'
    )

    def tax(self, product: Product):
        return product.unit_price + 10

    # likes_count = serializers.SerializerMethodField(
    #     method_name='likes'
    # )

    # def likes(self, product: Product):
    #     if Likes.objects.filter(pk=product.id).exists():
    #         like_count = Likes.objects.get(pk=product.id)
    #         return like_count.count
    #     else:
    #         return 0

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title", "unit_price", "collection", "customers_liked", "likes_count", ]

        likes_count = serializers.SerializerMethodField(
            method_name='likes'
        )

        # def likes(self, product: Product):
        #     queryset = Likes.objects.filter(pk=product.id)
        #     like_count = queryset.get()
        #     return like_count
