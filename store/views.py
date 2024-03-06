from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.generics import GenericAPIView
from rest_framework import status

from django.shortcuts import reverse as django_reverse
from .models import *
from .serializers import *
from django.shortcuts import redirect


class RootAPIView(APIView):
    def get(self, request):
        return Response({
            'product': reverse('store:product_root', request=request),
            'collection': reverse('store:collections_list', request=request),
        })


class ProductRoot(APIView):
    def get(self, request):
        return Response({
            'product_list': reverse('store:products_list', request=request),
            'product_create': reverse('store:create_product', request=request),
            'product_update': "store/product/update/the id of the product you want to update",
            'product_patch': "store/product/patch/the id of the product you want to patch",
            'most_popular': reverse('store:products_list_most_popular', request=request),

        })


class ProductList(APIView):
    def get(self, request):
        if self.request.query_params.get("order"):
            queryset = Product.objects.select_related('collection').all().order_by(
                self.request.query_params.get("order"))
        else:
            queryset = Product.objects.select_related('collection').all()
        serialized_queryset = ProductSerializer(queryset, many=True, context={'request': request})
        print(self.request.query_params.get('a'), "sadfadsfasdfsaf")
        return Response(serialized_queryset.data)


class ProductsListMostPopular(APIView):
    def get(self, request):
        most_popular_queryset = Likes.objects.values('product__title', 'product__id').annotate(
            likes_count=Count('id'),
            date_liked=TruncDate('date_liked')
        ).order_by('-likes_count')
        return Response({
            "most_popular_queryset": most_popular_queryset

        })


class ProductSingle(APIView):
    def get(self, request, pk):
        queryset = Product.objects.get(pk=pk)
        serialized_queryset = ProductSerializer(queryset, context={'request': request})
        return Response(serialized_queryset.data)


class Collections(APIView):
    def get(self, request):
        queryset = Collection.objects.all()
        serialized_queryset = CollectionSerializer(queryset, many=True)
        return Response(serialized_queryset.data)


class CollectionDetails(APIView):
    def get(self, request, pk):
        queryset = Collection.objects.get(pk=pk)
        serialized_queryset = CollectionSerializer(queryset)
        return Response(serialized_queryset.data)


class CreateProduct(APIView):
    serializer_class = ProductSerializer

    def get_serializer(self, instance=None):
        if instance:
            return self.serializer_class(instance)
        return ItemSerializer()

    def get(self, request):
        return Response(
            {
                "description": "to create a product fill this fields:"
                , "title": ""
                , "unit_price": ""
                , "collection": ""
            }
        )

    def post(self, request):
        item_title = request.data["title"]
        item_unit_price = int(request.data["unit_price"])
        item_collection = int(request.data["collection"])
        if Product.objects.filter(title=item_title).exists():
            raise serializers.ValidationError("this object already exists")
        # if item_collection > Collection.objects.all().count():
        #     raise serializers.ValidationError("no such a collection")
        else:
            new_product = Product.objects.create(title=item_title, unit_price=item_unit_price,
                                                 collection=Collection.objects.get(id=item_collection))
            new_product.save()

            return redirect("store:single_product", pk=new_product.id)


class LikeProduct(APIView):

    def get(self, request):
        return Response(
            {
                "description": "to like a product fill this fields:"
                , "product_id": ""
                , "customer_id": ""
            }
        )

    def post(self, request):
        liked_product = Product.objects.get(id=(int(request.data["product_id"])))
        customer_liked_id = Customer.objects.get(id=int(request.data["customer_id"]))
        if Likes.objects.filter(product=liked_product).exists():

            new = Likes.objects.create(product=liked_product, customer=customer_liked_id)
            new.save()
            if liked_product.likes_count is not None:
                liked_product.likes_count += 1
            else:
                liked_product.likes_count = 1
            liked_product.customers_liked.add(customer_liked_id)
            liked_product.save()
            return redirect("store:single_product", pk=liked_product.id)
        else:
            new = Likes.objects.create(product=liked_product, customer=customer_liked_id)
            new.save()
            liked_product.likes_count = 1
            liked_product.save()

            return redirect("store:single_product", pk=liked_product.id)


class UpdateProduct(APIView):
    def get(self, request, pk):
        item = Product.objects.get(pk=pk)
        serialized_item = ProductSerializer(item, context={'request': request})
        return Response(serialized_item.data)

    def post(self, request, pk):
        item = Product.objects.get(pk=pk)
        data = ItemSerializer(instance=item, data=request.data)

        if data.is_valid():
            data.save()
            return Response(data.data)


class PatchProduct(APIView):
    def get(self, request, pk):
        item = Product.objects.get(pk=pk)
        serialized_item = ProductSerializer(item, context={'request': request})
        return Response(serialized_item.data)

    def post(self, request, pk):
        item = Product.objects.get(pk=pk)
        data = ItemSerializer(item, data=request.data, partial=True)
        print(request.data["title"])
        if data.is_valid():
            data.save()
            return Response(data.data)
