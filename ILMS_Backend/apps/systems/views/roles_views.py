from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

import settings
from utils.list_pages import CusResponse, MySearchFilter, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import RolesInfo
from ..serializers import RolesSerializerAnti, RolesSerializer
from ..utils import RoleFilterSet, CheckRoleNameFilter


# 角色读视图集
class RolesReadViews(ReadModelViewSetPlus):
    """角色读视图集"""

    queryset = RolesInfo.objects.filter(~Q(pk=1))
    serializer_class = RolesSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = RoleFilterSet
    pagination_class = CusResponse
    search_fields = ['name', 'desc']


# 角色写视图集
class RolesWriteViews(WriteModelViewSetPlus):
    """角色写视图集"""

    queryset = RolesInfo.objects.filter(~Q(pk=1))
    serializer_class = RolesSerializerAnti

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('name'):
            return CusResponse.get_response(success=False, message='缺少角色名称', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)


# 检查角色名称是否重复
class CheckRoleName(GenericAPIView):
    """检查角色名称是否重复"""

    queryset = RolesInfo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckRoleNameFilter

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
            return CusResponse.get_response(data=1, message='该角色名称已存在！')


if __name__ == '__main__':
    pass
