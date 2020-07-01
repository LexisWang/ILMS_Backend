from django_filters.rest_framework import DjangoFilterBackend

from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import OrdFundsInfo
from ..serializers import OrderFundSerializerAnti, OrderFundSerializer
from ..utils import OrdFundsFilterSet


# 订单款项读视图集
class OrdFundReadViews(ReadModelViewSetPlus):
    """订单款项读视图集"""

    queryset = OrdFundsInfo.objects.all()
    serializer_class = OrderFundSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = OrdFundsFilterSet
    pagination_class = CusResponse
    # search_fields = ['code', 'name']

    def get_queryset(self):
        return self._get_queryset(self.request.user, queryset=self.queryset, model=OrdFundsInfo)


# 订单款项写视图集
class OrdFundWriteViews(WriteModelViewSetPlus):
    """订单款项写视图集"""

    queryset = OrdFundsInfo.objects.all()
    serializer_class = OrderFundSerializerAnti


if __name__ == '__main__':
    pass
