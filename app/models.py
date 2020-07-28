from django.db import models


class Notification(models.Model):
    notification_type = models.CharField(max_length=128, blank=True, null=True)
    order_id = models.BigIntegerField()
    data = models.CharField(max_length=32768)

    class Meta:
        db_table = "app_notification"
        verbose_name = "notification"


class Item(models.Model):
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=512)
    price = models.PositiveIntegerField()
    photo_url = models.CharField(max_length=4096, blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    expiration = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = "app_item"
        verbose_name = "item"


class Order(models.Model):
    app_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    order_id = models.BigIntegerField()

    class Meta:
        db_table = "app_order"
        verbose_name = "order"
