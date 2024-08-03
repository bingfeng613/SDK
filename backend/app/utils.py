from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.views import exception_handler

# todo：装饰器正常时候没生效
def custom_exception_handler(exc, ctx):
    # print("note")
    response = exception_handler(exc, ctx)
    if response is not None:
        data = {
            'code': response.status_code,
            'message': 'Success' if response.status_code == 200 else 'Error',
            'data': response.data if response.data else {}
        }
        return Response(data)
    # return Response({'data':'test'})

