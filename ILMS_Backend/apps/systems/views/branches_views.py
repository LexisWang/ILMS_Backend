from django.db.models import Q

import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

from utils.list_pages import CusResponse, MySearchFilter, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import BranchesInfo
from ..serializers import BranchesSerializerAnti, BranchesSerializer
from ..utils import BranchFilterSet, CheckBranNameFilter


# 分部读视图集
class BranchesReadViews(ReadModelViewSetPlus):
    """分部读视图集"""

    queryset = BranchesInfo.objects.filter(~Q(pk=1))
    serializer_class = BranchesSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = BranchFilterSet
    pagination_class = CusResponse
    search_fields = ['name', 'desc']


# 分部写视图集
class BranchesWriteViews(WriteModelViewSetPlus):
    """分部写视图集"""

    queryset = BranchesInfo.objects.filter(~Q(pk=1))
    serializer_class = BranchesSerializerAnti

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少分部名称', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


# 检查分部名称是否重复
class CheckBranName(GenericAPIView):
    """检查分部名称是否重复"""

    queryset = BranchesInfo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckBranNameFilter

    def get(self, request, *args, **kwargs):
        pk = self.request.query_params.get('pk')
        if pk and pk.isdigit():
            pk = int(pk)
        name = self.request.query_params.get('name')
        try:
            pk_, name_ = self.queryset.values_list('pk', 'name').get(name=name)
        except Exception as e:
            return CusResponse.get_response(data=0)
        if pk == pk_:
            return CusResponse.get_response(data=0)
        else:
            return CusResponse.get_response(data=1, message='该分部名称已存在！')


if __name__ == '__main__':
    pass
