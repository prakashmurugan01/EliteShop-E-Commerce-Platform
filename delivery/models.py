from django.db import models
from orders.models import Order

class DeliveryTracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    current_location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking - {self.order.order_number}"

class DeliveryStatusUpdate(models.Model):
    tracking = models.ForeignKey(DeliveryTracking, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20)
    location = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tracking.order.order_number} - {self.status}"

    class Meta:
        ordering = ['timestamp']