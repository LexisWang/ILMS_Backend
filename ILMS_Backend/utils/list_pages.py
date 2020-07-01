import datetime
import json
from copy import copy

from dateutil.relativedelta import relativedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, \
    ListModelMixin

import settings
from django.db.models import Q
from django.http import JsonResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from systems.models import BranchesInfo, RolesInfo, UsersInfo
from utils.menus_code import all_menus_list


class CustomControl(object):  # 自定义的各种控制
    def dispatch(self, request, *args, **kwargs):

        # # 提前验证用户，以便获取当前登陆的用户
        # _request = self.initialize_request(request, *args, **kwargs)
        #
        # # 如何是 admin 用户直接过
        # if _request.user.id == 1:
        #     pass
        # else:
        #     try:
        #         self._menus_control(redis_key=_request.user.id,
        #                             view_str=all_menus_list.get(self.request.path[1:]).get(self.action))
        #     except PermissionDenied as e:
        #         return JsonResponse({"success": False, 'massage': e.detail, "code": settings.FALSE_CODE, 'data': None})
        #
        # # 继续执行 dispatch 函数
        return super().dispatch(request, *args, **kwargs)

    def _response(self, data=None, success=True, message=None, code=settings.SUCCESS_CODE):
        return {'success': success, 'message': message, 'code': code, 'data': data}

    def _get_queryset(self, user, queryset, model):
        return queryset
        # level = min(set(list(user.roles.all().values_list('level', flat=True))))
        # if level == 1:
        #     if model in [BranchesInfo, RolesInfo, UsersInfo]:
        #         return queryset.filter(~Q(pk=1))
        #     else:
        #         return queryset.all()
        # elif level == 2:
        #     if hasattr(model, 'username'):
        #         return queryset.filter((Q(creator__bran=user.bran) | Q(bran=user.bran)) & ~Q(pk=1))
        #     elif model in [BranchesInfo, RolesInfo]:
        #         return queryset.filter(Q(creator__bran=user.bran) & ~Q(pk=1))
        #     else:
        #         return queryset.filter(creator__bran=user.bran)
        # elif level == 3:
        #     if hasattr(model, 'username'):
        #         return queryset.filter((Q(creator__bran=user.bran) | Q(id=user.id)) & ~Q(pk=1))
        #     elif model in [BranchesInfo, RolesInfo]:
        #         return queryset.filter(Q(creator=user) & ~Q(pk=1))
        #     else:
        #         return queryset.filter(creator=user)

    def _menus_control(self, redis_key, view_str):
        # 获取 Redis 中的 权限缓存
        redis_conn = get_redis_connection('default')
        redis_menus = redis_conn.get(redis_key)

        # Redis 中的 menus 已过期
        if not redis_menus:
            raise PermissionDenied(detail='缓存已过期', code=settings.FALSE_CODE)

        # 判断是否有权限
        request_user_menus = json.loads((redis_menus.decode()))
        if not request_user_menus.get(view_str):
            raise PermissionDenied(detail='无访问权限', code=settings.FALSE_CODE)


class ReadModelViewSetPlus(CustomControl,  # 自定义的读取数据集
                           RetrieveModelMixin,
                           ListModelMixin,
                           GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(self._response(serializer.data))


class WriteModelViewSetPlus(CustomControl,  # 自定义的写入数据集
                            CreateModelMixin,
                            UpdateModelMixin,
                            DestroyModelMixin,
                            GenericViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self._response(serializer.data), status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(self._response(serializer.data))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(self._response(), status=status.HTTP_204_NO_CONTENT)


class CusResponse(PageNumberPagination):
    page_query_description = '查询第几页信息'
    page_size_query_description = '每页数据条数'

    page_size = 5  # 默认每页容量
    page_query_param = 'page'  # 前端请求的页数
    page_size_query_param = 'pagesize'  # 前端请求的每页容量
    max_page_size = 10  # 前端最多能设置的每页数量

    def get_paginated_response(self, data):
        return Response({
            "success": True,
            "code": None,
            'page': {
                'page': self.page.number,  # 当前第几页
                'pagesize': int(self.request.query_params.get('pagesize')) if self.request.query_params.get(
                    'pagesize') else self.page_size,  # 每页数据量
                'count': self.page.paginator.count,  # 数据总量
                'pages': self.page.paginator.num_pages,  # 总页数
            },
            'data': data
        })

    @staticmethod
    def get_response(data=None, success=True, message=None, code=settings.SUCCESS_CODE):
        return Response({
            "success": success,
            'massage': message,
            "code": code,
            'data': data
        })


class MySearchFilter(SearchFilter):
    search_description = '模糊搜索关键字'


class MyOrderingFilter(OrderingFilter):
    ordering_description = '排序字段，格式如：-customer_code(反序)， customer_code(正序)'


# 自定义过滤后端类
class CustomDjangoFilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        query_params = copy(request.query_params)  # type: dict

        order_time_start = query_params.get('order_time_start')
        order_time_end = query_params.get('order_time_end')
        if order_time_end:  # 如果有结束时间,则结束时间加一天
            order_time_end = datetime.datetime.strptime(order_time_end, '%Y-%m-%d') + datetime.timedelta(days=1)
        if order_time_start and not order_time_end:  # 如有开始时间,无结束时间,则 '结束时间' 为 '开始时间' 加 一年
            order_time_end = datetime.datetime.strptime(order_time_start, '%Y-%m-%d') + relativedelta(years=1)
        if order_time_end and not order_time_start:  # 如有结束时间,无开始时间,则 '开始时间' 为 '结束时间' 减 一年
            order_time_start = order_time_end - relativedelta(years=1)
        if not order_time_start and not order_time_end:  # 如果都没有,则 '结束时间' 为今天, '开始时间' 为一年前的今天
            end_time = datetime.datetime.now() + datetime.timedelta(days=1)
            start_time = end_time - relativedelta(years=1)
            order_time_start = start_time.strftime('%Y-%m-%d')
            order_time_end = end_time.strftime('%Y-%m-%d')

        # 重新给过滤参数赋值
        query_params.update({'order_time_start': order_time_start, 'order_time_end': order_time_end})

        return {
            'data': query_params,
            'queryset': queryset,
            'request': request,
        }
