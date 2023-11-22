from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from django.http import JsonResponse
from .models import Vendor
from datetime import timezone
from rest_framework import status
from rest_framework import generics
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


@api_view(['POST', 'GET'])
def vendor_list_create(request):
    if request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def vendor_list_html(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})

def vendor_detail_html(request, vendor_code):
    vendor = get_object_or_404(Vendor, pk=vendor_code)
    return render(request, 'vendor_detail.html', {'vendor': vendor})

@api_view(['POST'])
def create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_purchase_orders(request):
    vendor_id = request.query_params.get('vendor_id', None)
    if vendor_id:
        purchase_orders = PurchaseOrder.objects.filter(vendor__id=vendor_id)
    else:
        purchase_orders = PurchaseOrder.objects.all()

    serializer = PurchaseOrderSerializer(purchase_orders, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_detail(request, po_id):
    # Retrieve the purchase order
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

    if request.method == 'GET':
        # Retrieve details of the purchase order
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the purchase order
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the purchase order
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    # Calculate performance metrics using model methods
    on_time_delivery_rate = vendor.calculate_on_time_delivery_rate()
    quality_rating_avg = vendor.calculate_quality_rating_avg()
    average_response_time = vendor.calculate_average_response_time()
    fulfillment_rate = vendor.calculate_fulfillment_rate()

    # Serialize the vendor data
    serializer = VendorSerializer(vendor)

    return Response({
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate,
    })

@api_view(['POST', 'GET'])
def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)

    # Check if acknowledgment_date is not already set
    if not purchase_order.acknowledgment_date:
        # Update acknowledgment_date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Recalculate average_response_time
        vendor = purchase_order.vendor
        vendor.calculate_average_response_time()
        vendor.save()

        return Response({'message': 'Purchase order acknowledged successfully.'})
    else:
        return Response({'error': 'Purchase order has already been acknowledged.'}, status=status.HTTP_400_BAD_REQUEST)