from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

import settings
from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import Cities
from ..serializers import CitySerializerAnti, CitySerializer
from ..utils import CityFilter, CitiesFilterSet


# 城市读视图集
class CitiesReadViews(ReadModelViewSetPlus):
    """城市读视图集"""

    queryset = Cities.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = CitiesFilterSet
    pagination_class = CusResponse
    search_fields = ['code', 'name']


# 城市写视图集
class CitiesWriteViews(WriteModelViewSetPlus):
    """城市写视图集"""

    queryset = Cities.objects.all()
    serializer_class = CitySerializerAnti

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('code'):
            return CusResponse.get_response(success=False, message='缺少城市代码', code=settings.FALSE_CODE)
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少城市名称', code=settings.FALSE_CODE)
        if not self.request.data.get('county'):
            return CusResponse.get_response(success=False, message='缺少国家ID', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


# 城市检查
class CheckCity(GenericAPIView):

    queryset = Cities.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CityFilter

    def get(self, request, *args, **kwargs):
        """校验城市是否重复"""
        code = self.request.query_params.get('code')
        name = self.request.query_params.get('name')
        county = self.request.query_params.get('county')

        pk = self.request.query_params.get('pk')
        if pk and pk.isdigit():
            pk = int(pk)
        if county and county.isdigit():
            county = int(county)
        else:
            return CusResponse.get_response(success=False, message='缺少国家id错误')

        if code and not name:
            try:
                pk_, code_ = self.queryset.values_list('pk', 'code').filter(
                    county=county).get(code=code)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该城市代码已存在！')
        elif name and not code:
            try:
                pk_, name_ = self.queryset.values_list('pk', 'name').filter(
                    county=county).get(name=name)
            except Exception as e:
                return CusResponse.get_response(data=0)
            if pk == pk_:
                return CusResponse.get_response(data=0)
            else:
                return CusResponse.get_response(data=1, message='该城市名称已存在！')
        else:
            return CusResponse.get_response(success=False, message='参数有误')


if __name__ == '__main__':
    pass
