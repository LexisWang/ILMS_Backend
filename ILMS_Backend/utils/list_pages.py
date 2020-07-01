import datetime
import json
import os
from copy import copy

from dateutil.relativedelta import relativedelta
from django.utils.encoding import escape_uri_path
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, \
    ListModelMixin
from pandas import DataFrame, ExcelWriter, Series

import settings
from django.db.models import Q
from django.http import JsonResponse, FileResponse
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


# 自定义导出 list 视图
class CustomExportListView(ListAPIView):
    # 新增几个类属性
    excel_name = None  # 单数
    sheet_names = None  # list
    total_columns = None  # list
    sub__models = None  # list
    sub_serializers = None  # list
    columns_names = None  # list(list)
    sub_total = False  # 标识符
    ini = 0

    # 主调函数
    def list(self, request, *args, **kwargs):
        self.group_word = self.request.query_params.get('group_word')
        dict_data = [self.__old_dict_single()]
        if self.sub__models:
            for i in range(len(self.sub__models)):
                parent_ids = [j.get('pk') for j in dict_data[i]]
                dict_data.append(self.sub_serializers[i](self.sub__models[i].objects.filter(order__in=parent_ids), many=True).data)
        dataframe = self.__dict2dataframe(dict_data)
        last_dataframe = self.transform_dataframe(dataframe)
        response = self.__dataframe2excel(last_dataframe)
        return response

    # 获取主序列化后的数据 dict
    def __old_dict_single(self):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    # 序列化后的数据转为 DataFrame
    def __dict2dataframe(self, dict_data):
        return [DataFrame(dict_datum) for dict_datum in dict_data]

    # 转换 DataFrame 数据
    def transform_dataframe(self, dataframe):
        if self.sub_total:
            dataframe[0] = self.__add_sub_total(dataframe[0])
        else:
            dataframe[0] = self.__add_total(dataframe[0])
        for i in range(len(dataframe)):
            if 'pk' in dataframe[i].columns:
                dataframe[i].drop('pk', axis=1, inplace=True)
            else:
                dataframe[i].reset_index(inplace=True)
                dataframe[i].drop('id', axis=1, inplace=True)
            dataframe[i].columns = self.columns_names[i]
        return dataframe

    # 给表添加 总计
    def __add_total(self, dataframe):
        dataframe = dataframe.append(dataframe[self.total_columns].sum().T, ignore_index=True)
        dataframe.reset_index(inplace=True)
        dataframe['index'] = dataframe['index'] + 1
        dataframe.iloc[-1, 0] = '总计'
        return dataframe

    # 给表添加 小计 和 总计
    def __add_sub_total(self, dataframe):
        # 1.对表数据排序
        dataframe = dataframe.sort_values(self.group_word, ignore_index=True)

        # 2.计算总计
        total_data = dataframe[self.total_columns].sum().T

        # 3.表数据分组求和
        total_columns = [self.group_word]
        total_columns.extend(self.total_columns)
        subtotal = dataframe[total_columns].groupby(self.group_word).sum().T
        subtotal.loc[self.group_word] = subtotal.columns

        # 5.将分组数据插入到原表数据中
        # 求出分组求和数据的 'index' 在 原表中个的 'location'
        location = {}
        for column_name in subtotal.columns:
            location.update({column_name: dataframe[dataframe[self.group_word] == column_name].index.tolist()[-1] + 1})
        # 对应位置插入数据
        dataframe = dataframe.T
        for index, value in enumerate(location):
            dataframe.insert(loc=location.get(value), column='小计', value=subtotal[value], allow_duplicates=True)
        # 重排表的 'index'
        dataframe = dataframe.T
        dataframe.reset_index(inplace=True)
        dataframe['index'] = dataframe['index'].apply(self.__reset_index)

        # 6.在原表末尾加入总计行
        dataframe = dataframe.append(total_data, ignore_index=True)
        dataframe.iloc[-1, 0] = '总计'

        # 8.返回表数据
        return dataframe

    # 重排表的 序号
    def __reset_index(self, value):
        if value == '小计' or value == '合计':
            self.ini = 0
            return value
        else:
            self.ini += 1
            return self.ini

    # 表单导出
    def __dataframe2excel(self, dataframe):
        writer = ExcelWriter('tmp.xlsx')
        for i in range(len(dataframe)):
            dataframe[i].to_excel(writer, sheet_name=self.sheet_names[i], index=False)
        writer.save()
        file = open('tmp.xlsx', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment;filename={escape_uri_path(self.excel_name)}'
        os.remove('tmp.xlsx')
        return response
