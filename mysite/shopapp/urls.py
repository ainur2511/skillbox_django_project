from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductsDetailsView,
                    ProductListView,
                    OrderListView,
                    OrderDetailView,
                    ProductCreateView,
                    OrderCreateView,
                    ProductUpdateView,
                    ProductDeleteView,
                    OrderUpdateView,
                    OrderDeleteView,
                    OrdersDataExportView,
                    HelloView,
                    ProductViewSet,
                    OrderViewSet,
                    LastProductsFeed,
                    )


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)


app_name = 'shopapp'
urlpatterns = [
    path("products/", ProductListView.as_view(), name='products_list'),
    path("products/create/", ProductCreateView.as_view(), name='product_create'),
    path("products/<int:pk>/", ProductsDetailsView.as_view(), name='products_details'),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name='products_update'),
    path("products/<int:pk>/archive/", ProductDeleteView.as_view(), name='products_delete'),
    path("products/latest/feed/", LastProductsFeed(), name='products_latest_feed'),
    path("orders/", OrderListView.as_view(), name='order_list'),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name='orders_detail'),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name='orders_update'),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name='orders_delete'),
    path("orders/create/", OrderCreateView.as_view(), name='order_create'),
    path("orders/export/", OrdersDataExportView.as_view(), name='orders_export'),
    path('hello/', HelloView.as_view(), name='hello'),
    path('api', include(router.urls))

]
