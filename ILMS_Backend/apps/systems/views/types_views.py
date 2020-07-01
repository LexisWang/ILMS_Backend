from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

import settings
from utils.list_pages import CusResponse, MySearchFilter, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import DataDictType
from ..serializers import DictTypesSerializer
from ..utils import CheckTypeFilter


# 字典类型读视图集
class TypesReadViews(ReadModelViewSetPlus):
    """字典类型读视图集"""

    queryset = DataDictType.objects.all()
    serializer_class = DictTypesSerializer
    filter_backends = [MySearchFilter]
    pagination_class = CusResponse
    search_fields = ['code', 'name']


# 字典类型写视图集
class TypesWriteViews(WriteModelViewSetPlus):
    """字典类型写视图集"""

    queryset = DataDictType.objects.all()
    serializer_class = DictTypesSerializer

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('code'):
            return CusResponse.get_response(success=False, message='缺少类型代码', code=settings.FALSE_CODE)
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少类型名称', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


class CheckType(GenericAPIView):
    queryset = DataDictType.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckTypeFilter

    def get(self, request, *args, **kwargs):
        """校验字典类型是否重复"""
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
                return CusResponse.get_response(data=1, message='该类型代码已存在！')
        elif name and not code:
            try:
                pk_, county_name_ = self.queryset.values_list('pk', 'name').get(
                    name=name)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该类型名称已存在！')
        else:
            return CusResponse.get_response(success=False, message='参数有误')


if __name__ == '__main__':
    pass
