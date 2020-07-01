from django_filters.rest_framework import DjangoFilterBackend

from funds.utils import CustomsFundsFilterSet
from utils.list_pages import ReadModelViewSetPlus, WriteModelViewSetPlus, MySearchFilter, CusResponse
from ..models import CustomsFundsInfo
from ..serializers import CustomsFundSerialAnti, CustomsFundSerial


# 清关款项读视图集
class CustomsFundReadViews(ReadModelViewSetPlus):
    """清关款项读视图集"""

    queryset = CustomsFundsInfo.objects.all()
    serializer_class = CustomsFundSerial
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = CustomsFundsFilterSet
    pagination_class = CusResponse
    search_fields = ['code', 'name']

    def get_queryset(self):
        return self._get_queryset(self.request.user, queryset=self.queryset, model=CustomsFundsInfo)


# 清关款项写视图集
class CustomsFundWriteViews(WriteModelViewSetPlus):
    """清关款项写视图集"""

    queryset = CustomsFundsInfo.objects.all()
    serializer_class = CustomsFundSerialAnti


if __name__ == '__main__':
    pass