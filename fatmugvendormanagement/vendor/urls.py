from django.urls import path
from vendor import views

urlpatterns = [
    path('api/vendors/', views.vendor_list_create, name='vendor-list-create'),
    path('api/vendors/<int:vendor_id>/', views.vendor_detail, name='vendor-detail'),
    path('vendors/', views.vendor_list_html, name='vendor-list-html'),
    path('vendors/<int:vendor_id>/', views.vendor_detail_html, name='vendor-detail-html'),
    path('api/vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor-performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge-purchase-order'),
]