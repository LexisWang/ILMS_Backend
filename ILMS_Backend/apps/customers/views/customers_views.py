from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

import settings
from systems.models import DataDictsValue, UsersInfo, DataDictType
from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..serializers import CusCreUpdSerAnti, CusCreUpdSer
from ..models import CustomersInfo
from ..utils import CustomersFilterSet, CusCodeFilterSet


# 客户方读视图集
class CustomersReadViews(ReadModelViewSetPlus):
    """客户方读视图集"""

    queryset = CustomersInfo.objects.all()
    serializer_class = CusCreUpdSer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = CustomersFilterSet
    pagination_class = CusResponse
    search_fields = ['code', 'name', 'president_name', 'customer_address', 'manage_directions', 'remark_comment']

    def get_queryset(self):
        return self._get_queryset(self.request.user, queryset=self.queryset, model=CustomersInfo)


# 客户方写视图集
class CustomersWriteViews(WriteModelViewSetPlus):
    """客户方写视图集"""

    queryset = CustomersInfo.objects.all()
    serializer_class = CusCreUpdSerAnti

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('code'):
            return CusResponse.get_response(success=False, message='缺少客户代码', code=settings.FALSE_CODE)
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少客户名称', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


class CheckCusCode(GenericAPIView):
    """检查客户代码是否重复"""

    queryset = CustomersInfo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CusCodeFilterSet

    def get(self, request, *args, **kwargs):
        pk = self.request.query_params.get('pk')
        if pk and pk.isdigit():
            pk = int(pk)
        code = self.request.query_params.get('code')
        name = self.request.query_params.get('name')
        if code and not name:
            try:
                pk_, code_ = self.queryset.values_list('pk', 'code').get(
                    code=code)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该客户代码已存在！')
        elif name and not code:
            try:
                pk_, county_name_ = self.queryset.values_list('pk', 'name').get(
                    name=name)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该客户名称已存在！')
        else:
            return CusResponse.get_response(success=False, message='参数有误')


# 获取新增客户时的选项列表
class GetCusOptionsView(GenericAPIView):
    """获取新增客户时的选项列表"""

    def get(self, request):
        rank_type_id = DataDictType.objects.get(code=settings.CUS_RANK).id
        return CusResponse.get_response(data={
            'ranks': DataDictsValue.objects.values('id', 'code', 'name').filter(status=1, type=rank_type_id),
            'salesman': UsersInfo.objects.values('id', 'account', 'username').filter(~Q(id=1) & Q(status=1)),
            'services': UsersInfo.objects.values('id', 'account', 'username').filter(~Q(id=1) & Q(status=1)),
        })


if __name__ == '__main__':
    pass
