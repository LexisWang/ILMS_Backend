from django_filters.rest_framework import DjangoFilterBackend

from utils.list_pages import ReadModelViewSetPlus, WriteModelViewSetPlus, MySearchFilter, CusResponse
from ..models import OtherFundsInfo
from ..serializers import OthFundsSerializer, OthFundsSerializerAnti
from ..utils import OthersFundsFilterSet


# 其他款项读视图集
class OthersFundReadViews(ReadModelViewSetPlus):
    """其他款项读视图集"""

    queryset = OtherFundsInfo.objects.all()
    serializer_class = OthFundsSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = OthersFundsFilterSet
    pagination_class = CusResponse
    search_fields = ['code', 'name']

    def get_queryset(self):
        return self._get_queryset(self.request.user, queryset=self.queryset, model=OtherFundsInfo)


# 其他款项写视图集
class OthersFundWriteViews(WriteModelViewSetPlus):
    """其他款项写视图集"""

    queryset = OtherFundsInfo.objects.all()
    serializer_class = OthFundsSerializerAnti

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


if __name__ == '__main__':
    pass
