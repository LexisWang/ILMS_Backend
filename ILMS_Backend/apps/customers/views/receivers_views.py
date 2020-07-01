from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

import settings
from systems.models import Countries, Cities
from utils.list_pages import CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..serializers import ReceiversSerializerAnti, ReceiversSerializer
from ..models import ReceiversInfo, CustomersInfo
from ..utils import ReceiversFilterSet, RecCodeFilterSet, RecCityFilter


# 收货方读视图集
class ReceiversReadViews(ReadModelViewSetPlus):
    """收货方读视图集"""

    queryset = ReceiversInfo.objects.all()
    serializer_class = ReceiversSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceiversFilterSet
    pagination_class = CusResponse
    search_fields = ['code', 'name', 'company', 'address']


# 收货方读视图集
class ReceiversWriteViews(WriteModelViewSetPlus):
    """收货方读视图集"""

    queryset = ReceiversInfo.objects.all()
    serializer_class = ReceiversSerializerAnti

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('code'):
            return CusResponse.get_response(success=False, message='缺少收货方代码', code=settings.FALSE_CODE)
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少收货方名称', code=settings.FALSE_CODE)
        if not self.request.data.get('customer'):
            return CusResponse.get_response(success=False, message='缺少客户ID', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


class CheckRecCode(GenericAPIView):
    """检查收货方代码是否重复"""

    queryset = ReceiversInfo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecCodeFilterSet

    def get(self, request, *args, **kwargs):
        code = self.request.query_params.get('code')
        name = self.request.query_params.get('name')
        customer = self.request.query_params.get('customer')

        pk = self.request.query_params.get('pk')
        if pk and pk.isdigit():
            pk = int(pk)
        if customer and customer.isdigit():
            customer = int(customer)
        else:
            return CusResponse.get_response(success=False, message='缺客户id错误')

        if code and not name:
            try:
                pk_, code_ = self.queryset.values_list('pk', 'code').filter(
                    customer=customer).get(code=code)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该字典值代码已存在！')
        elif name and not code:
            try:
                pk_, name_ = self.queryset.values_list('pk', 'name').filter(
                    customer=customer).get(name=name)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该字典值名称已存在！')
        else:
            return CusResponse.get_response(success=False, message='参数有误')


# 获取新增收货方时的选项列表
class RecOptionsView(GenericAPIView):
    """获取新增收货方时的选项列表"""

    def get(self, request):
        return CusResponse.get_response(data={
            'customers': CustomersInfo.objects.values('id', 'code', 'name').all(),
            'counties': Countries.objects.values('id', 'code', 'name').all(),
        })


# 获取新增收货方时的选项列表(城市)
class CityOptionsView(GenericAPIView):
    """获取新增收货方时的选项列表(城市)"""

    queryset = Cities.objects.filter(status=1)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecCityFilter

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return CusResponse.get_response(data={
            'cities': queryset.values('id', 'code', 'name'),
        })


if __name__ == '__main__':
    pass
