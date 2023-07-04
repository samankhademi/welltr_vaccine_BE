from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .data import data


# Create your views here.
def get_payload(payload, req_id, req_time):
    return {
        "payload": payload,
        "request_id": req_id,
        "request_time": req_time,
        "status_code": 0,
        "status_message": ""
    }


class MocksViewset(APIView):
    http_method_names = ["post", "options"]

    def post(self, request, host_id, op_code, *args, **kwargs):
        return JsonResponse(
            get_payload(data[op_code], request.data.get("request_id"), request.data.get("request_time")),
            status=status.HTTP_200_OK)
