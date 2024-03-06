from django.urls import path
from . import views

app_name = 'store'

# URLConf
urlpatterns = [
    path('', views.RootAPIView.as_view(), name="api-root"),
    path('product/', views.ProductRoot.as_view(), name='product_root'),
    path('product/list', views.ProductList.as_view(), name='products_list'),
    path('product/list/best_sellers', views.ProductsListMostPopular.as_view(), name='products_list_most_popular'),
    path('product/<int:pk>', views.ProductSingle.as_view(), name='single_product'),
    path('product/create', views.CreateProduct.as_view(), name='create_product'),
    path('product/update/<int:pk>', views.UpdateProduct.as_view(), name='update_product'),
    path('product/patch/<int:pk>', views.PatchProduct.as_view(), name='patch_product'),
    path('collection/', views.Collections.as_view(), name='collections_list'),
    path('collection/<int:pk>/', views.CollectionDetails.as_view(), name="collection_details"),
    path('product/like', views.LikeProduct.as_view(), name='like_product'),


]
