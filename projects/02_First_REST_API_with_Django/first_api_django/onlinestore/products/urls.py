# from django.urls import path
# from .views import manufacturerListView, ProductDetailView

# urlpatterns = [
#     path("",ProductListView.as_view(), name="product-list"),
#     path("products/<int:pk>/",ProductDetailView.as_view(), name="product-view")
# ]

from django.urls import path
from .views import product_list, product_detail, manufacturer_list, manufacturer_detail

urlpatterns =[ 
    path("products/", product_list, name="product-list"),
    path("products/<int:pk>", product_detail, name="produc-detail"),
    path("manufacturers/", manufacturer_list, name="manufacturer-list"),
    path("manufacturers/<int:pk>", manufacturer_detail, name="manufacturer-detail"),
]