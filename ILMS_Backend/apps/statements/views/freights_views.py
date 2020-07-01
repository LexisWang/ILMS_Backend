from django.utils.encoding import escape_uri_path
from rest_framework.generics import ListAPIView
from rest_pandas import PandasView, PandasExcelRenderer

from business.models import FreightsInfo
from utils.list_pages import CustomDjangoFilterBackend, CusResponse
from ..utils import FreightStatementFilterSet
from ..serializers import FreightStatementSerial, FreightPandasSerializer


# 运单报表查询视图
class FreightReportQueryViews(ListAPIView):
    """订单报表查询视图"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = FreightStatementFilterSet
    pagination_class = CusResponse


# 运单报表导出视图
class FreightPandasViews(PandasView):
    """订单报表导出视图"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = FreightStatementFilterSet

    pandas_serializer_class = FreightPandasSerializer
    renderer_classes = [PandasExcelRenderer]

    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            return escape_uri_path("运单报表(查询)")
        else:
            return None


if __name__ == '__main__':
    pass
