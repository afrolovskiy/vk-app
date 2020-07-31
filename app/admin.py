from django.contrib import admin

from . import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "app_id", "user_id", "order_id", "created_at")
    readonly_fields = ("app_id", "user_id", "order_id", "created_at")


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "notification_type", "created_at")
    readonly_fields = ("order_id", "notification_type", "data", "created_at")
