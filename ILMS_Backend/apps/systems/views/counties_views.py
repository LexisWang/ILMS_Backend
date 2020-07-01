from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

import settings
from systems.serializers import CountySerializer
from systems.utils import CheckTypeFilter
from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import Countries


# 国家读视图集
class CountiesReadViews(ReadModelViewSetPlus):
    """国家读视图集"""

    queryset = Countries.objects.all()
    serializer_class = CountySerializer
    filter_backends = [MySearchFilter]
    pagination_class = CusResponse
    search_fields = ['code', 'name']


# 国家写视图集
class CountiesWriteViews(WriteModelViewSetPlus):
    """国家写视图集"""

    queryset = Countries.objects.all()
    serializer_class = CountySerializer

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('code'):
            return CusResponse.get_response(success=False, message='缺少国家代码', code=settings.FALSE_CODE)
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少国家名称', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


class CheckCounty(GenericAPIView):
    queryset = Countries.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckTypeFilter

    def get(self, request, *args, **kwargs):
        """校验国家是否重复"""
        data1 = [{'county': county.values('id', 'code', 'name'),
                  'cities': county.cities.values('id', 'code', 'name').all()} for county in
                 Countries.objects.prefetch_related('cities').all()]
        return CusResponse.get_response(data1)

        # pk = self.request.query_params.get('pk')
        # if pk and pk.isdigit():
        #     pk = int(pk)
        # code = self.request.query_params.get('code')
        # name = self.request.query_params.get('name')
        # if code and not name:
        #     try:
        #         pk_, code_ = self.queryset.values_list('pk', 'code').get(code=code)
        #     except Exception as e:
        #         return CusResponse.get_response(data=0)
        #     if pk == pk_:
        #         return CusResponse.get_response(data=0)
        #     else:
        #         return CusResponse.get_response(data=1, message='该国家代码已存在！')
        # elif name and not code:
        #     try:
        #         pk_, county_name_ = self.queryset.values_list('pk', 'name').get(name=name)
        #     except Exception as e:
        #         return CusResponse.get_response(data=0)
        #     if pk == pk_:
        #         return CusResponse.get_response(data=0)
        #     else:
        #         return CusResponse.get_response(data=1, message='该国家名称已存在！')
        # else:
        #     return CusResponse.get_response(success=False, message='参数有误')


if __name__ == '__main__':
    pass
