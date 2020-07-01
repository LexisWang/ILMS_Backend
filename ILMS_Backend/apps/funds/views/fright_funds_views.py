from django_filters.rest_framework import DjangoFilterBackend

from utils.list_pages import ReadModelViewSetPlus, WriteModelViewSetPlus, MySearchFilter, CusResponse

from ..serializers import FreFundsSerializer, FreFundsSerializerAnti
from ..models import FreFundsInfo
from ..utils import FreFundsFilterSet


# 运单款项读视图集
class FreFundReadViews(ReadModelViewSetPlus):
    """运单款项读视图集"""

    queryset = FreFundsInfo.objects.all()
    serializer_class = FreFundsSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = FreFundsFilterSet
    pagination_class = CusResponse
    search_fields = ['code', 'name']

    def get_queryset(self):
        return self._get_queryset(self.request.user, queryset=self.queryset, model=FreFundsInfo)


# 运单款项写视图集
class FreFundWriteViews(WriteModelViewSetPlus):
    """运单款项写视图集"""

    queryset = FreFundsInfo.objects.all()
    serializer_class = FreFundsSerializerAnti


if __name__ == '__main__':
    pass
