import re
import logging

from django.db import connection
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import BasePermission
from rest_framework.response import Response


logger = logging.getLogger('django')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view)


class MyPermission(BasePermission):
    """自定义的权限过滤"""

    def has_permission(self, request, view):
        return bool(
            (request.path_info in settings.SAFE_URL) or
            (request.user and request.user.is_authenticated)
        )


class MiddlewareMixin(object):
    """权限控制中间件Mixin扩展类"""

    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request, *args, **kwargs):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class RbacMiddleware(MiddlewareMixin):
    """检查用户的url请求是否是其权限范围内"""

    def process_request(self, request):
        request_url = request.path_info
        permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
        print('访问url', request_url)
        print('权限--', permission_url)

        # 如果请求url在白名单，放行
        for url in settings.SAFE_URL:
            if re.match(url, request_url):
                return None

        # 如果未取到permission_url, 重定向至登录；为了可移植性，将登录url写入配置
        # 另外，Login必须设置白名单，否则访问login会反复重定向
        if not permission_url:
            # return redirect(settings.LOGIN_URL)
            return None

        # 循环permission_url，作为正则，匹配用户request_url
        # 正则应该进行一些限定，以处理：/user/ -- /user/add/匹配成功的情况
        flag = False
        for url in permission_url:
            url_pattern = settings.REGEX_URL.format(url=url)
            if re.match(url_pattern, request_url):
                flag = True
                break
        if flag:
            return None
        else:
            # 如果是调试模式，显示可访问url
            if settings.DEBUG:
                return Response({'err_msg': '无权限，请尝试访问以下地址'})
            else:
                return Response({'err_msg': '无权限访问'})


def my_middleware(get_response):
    # print('init 被调用')
    def middleware(request):
        # print('before request 被调用')
        response = get_response(request)
        # print('after response 被调用')
        sql = connection.queries
        if len(sql) > 1:
            logger.info(sql)
        return response
    return middleware
