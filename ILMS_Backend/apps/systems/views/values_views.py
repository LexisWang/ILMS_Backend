from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

import settings
from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import DataDictsValue
from ..serializers import DictValuesSerializerAnti, DictValuesSerializer
from ..utils import DictValuesFilterSet, CheckValueFilter


# 字典值读视图集
class ValuesReadViews(ReadModelViewSetPlus):
    """字典值读视图集"""

    queryset = DataDictsValue.objects.all()
    serializer_class = DictValuesSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = DictValuesFilterSet
    pagination_class = CusResponse
    search_fields = ['code', 'name']


# 字典值写视图集
class ValuesWriteViews(WriteModelViewSetPlus):
    """字典值写视图集"""

    queryset = DataDictsValue.objects.all()
    serializer_class = DictValuesSerializerAnti

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('code'):
            return CusResponse.get_response(success=False, message='缺少字典值代码', code=settings.FALSE_CODE)
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少字典值名称', code=settings.FALSE_CODE)
        if not self.request.data.get('type'):
            return CusResponse.get_response(success=False, message='缺少字典类型ID', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


class CheckValue(GenericAPIView):
    queryset = DataDictsValue.objects.all()
    serializer_class = DictValuesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckValueFilter

    def get(self, request, *args, **kwargs):
        code = self.request.query_params.get('code')
        name = self.request.query_params.get('name')
        _type = self.request.query_params.get('type')

        pk = self.request.query_params.get('pk')
        if pk and pk.isdigit():
            pk = int(pk)
        if _type and _type.isdigit():
            _type = int(_type)
        else:
            return CusResponse.get_response(success=False, message='缺少类型id错误')

        if code and not name:
            try:
                pk_, code_ = self.queryset.values_list('pk', 'code').filter(
                    type=_type).get(code=code)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该字典值代码已存在！')
        elif name and not code:
            try:
                pk_, name_ = self.queryset.values_list('pk', 'name').filter(
                    type=_type).get(name=name)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该字典值名称已存在！')
        else:
            return CusResponse.get_response(success=False, message='参数有误')


if __name__ == '__main__':
    pass
