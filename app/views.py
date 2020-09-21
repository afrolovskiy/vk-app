import json
import hashlib

from django.conf import settings
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import models


CALLBACK_TEST_SUFFIX = "_test"

CALLBACK_GET_ITEM = "get_item"
CALLBACK_GET_ITEM_TEST = CALLBACK_GET_ITEM + CALLBACK_TEST_SUFFIX

CALLBACK_ORDER_STATUS_CHANGE = "order_status_change"
CALLBACK_ORDER_STATUS_CHANGE_TEST = CALLBACK_ORDER_STATUS_CHANGE + CALLBACK_TEST_SUFFIX

ORDER_STATUS_CHARGEABLE = "chargeable"
ORDER_STATUS_REFUNDED = "refunded"

ERROR_CODE_SIGNATURE_INVALID = 10
ERROR_CODE_ITEM_NOT_FOUND = 20
ERROR_CODE_STATUS_UNKNOWN = 101


def index(request):
    if settings.DEBUG:
        pretty_input = json.dumps(request.GET, sort_keys=True, indent=4, separators=(",", ": "))
        print("input: \n{}".format(pretty_input))

    return render(request, "index.html")


@csrf_exempt
def callback(request):
    if request.method != "POST":
        return HttpResponseNotFound()

    notif_type = request.POST["notification_type"]
    models.Notification.objects.create(
        notification_type=notif_type,
        order_id=request.POST["order_id"],
        data=json.dumps(request.POST, sort_keys=True),
    )

    sign = request.POST.get("sig")
    if calc_signature(request.POST) != sign:
        return ResponseError(ERROR_CODE_SIGNATURE_INVALID, "Некорректная подпись.", True)

    if settings.DEBUG:
        pretty_input = json.dumps(request.POST, sort_keys=True, indent=4, separators=(",", ": "))
        print("input: \n{}".format(pretty_input))

    if notif_type in (CALLBACK_GET_ITEM, CALLBACK_GET_ITEM_TEST):
        # See documentation at https://vk.com/dev/payments_getitem
        try:
            item = models.Item.objects.get(name=request.POST["item"])
        except models.Item.DoesNotExist:
            return ResponseError(ERROR_CODE_ITEM_NOT_FOUND, "Товар не найден.", True)

        data = {"item_id": item.id, "title": item.title, "price": item.price}
        if item.photo_url:
            data["photo_url"] = item.photo_url
        if item.expiration:
            data["expiration"] = item.expiration
        return ResponseOk(data)

    elif notif_type in (CALLBACK_ORDER_STATUS_CHANGE, CALLBACK_ORDER_STATUS_CHANGE_TEST):
        # See documentation at https://vk.com/dev/payments_status
        status = request.POST["status"]
        if status == ORDER_STATUS_CHARGEABLE:
            order = models.Order.objects.create(
                app_id=request.POST["app_id"],
                user_id=request.POST["user_id"],
                order_id=request.POST["order_id"],
            )
            return ResponseOk({"order_id": order.order_id, "app_order_id": order.id})
        elif status == ORDER_STATUS_REFUNDED:
            try:
                order = models.Order.objects.get(
                    app_id=request.POST["app_id"],
                    user_id=request.POST["user_id"],
                    order_id=request.POST["order_id"],
                )
            except models.Order.DoesNotExist:
                return ResponseError(ERROR_CODE_ITEM_NOT_FOUND, "Заказ не найден.", True)

            return ResponseOk({"order_id": order.order_id, "app_order_id": order.id})
        else:
            return ResponseError(ERROR_CODE_STATUS_UNKNOWN, "Неизвестный статус.")

    else:
        return HttpResponseNotFound()


def calc_signature(data):
    m = hashlib.md5()
    for k in sorted(data.keys()):
        if k != "sig":
            s = k + "=" + data[k]
            m.update(s.encode("utf-8"))
    m.update(settings.API_SECRET_KEY.encode("utf-8"))
    return m.hexdigest()


class ResponseOk(JsonResponse):
    def __init__(self, data):
        super().__init__({"response": data})


class ResponseError(JsonResponse):
    def __init__(self, err_code, err_msg, critical=False):
        data = {"error_code": err_code, "error_msg": err_msg}
        if critical:
            data["critical"] = critical
        super().__init__({"error": data})
