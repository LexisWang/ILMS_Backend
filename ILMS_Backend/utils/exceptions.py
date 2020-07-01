from django.http import Http404
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.views import exception_handler

import settings
from .list_pages import CusResponse


def cus_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, NotAuthenticated):
        return CusResponse.get_response(success=False, message='未提供登录信息，请登录！', code=settings.FALSE_CODE)
    if isinstance(exc, AuthenticationFailed):
        return CusResponse.get_response(success=False, message='登录信息已过期，请重新登录！', code=settings.FALSE_CODE)
    if isinstance(exc, Http404):
        return CusResponse.get_response(success=False, message='该资源不存在！', code=settings.FALSE_CODE)
    return CusResponse.get_response(success=False, message=str(exc), code=settings.FALSE_CODE)
