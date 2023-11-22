from django.db import models
from datetime import timedelta
from django.db.models import F, ExpressionWrapper, fields

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact = models.IntegerField()
    address = models.CharField(max_length=255)
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)  
        
    def calculate_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')

        on_time_delivery_orders = completed_orders.filter(delivery_date__lte=F('acknowledgment_date'))
        total_completed_orders = completed_orders.count()
        on_time_delivery_rate = (on_time_delivery_orders.count() / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        return on_time_delivery_rate

    def calculate_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')

        quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0

        return quality_rating_avg

    def calculate_average_response_time(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')

        response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())
        ).values_list('response_time', flat=True)
        average_response_time = sum(response_times, timedelta()) / len(response_times) if len(response_times) > 0 else 0

        return average_response_time

    def calculate_fulfillment_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')

        fulfilled_orders = completed_orders.filter(issue_date__lte=F('acknowledgment_date'))
        total_completed_orders = completed_orders.count()
        fulfillment_rate = (fulfilled_orders.count() / total_completed_orders) * 100 if total_completed_orders > 0 else 0

        return fulfillment_rate

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.vendor