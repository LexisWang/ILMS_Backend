from django.utils.encoding import escape_uri_path
from rest_framework.generics import ListAPIView
from rest_pandas import PandasView, PandasExcelRenderer

from business.models import FreightsInfo, OrdersInfo, GoodsInfo
from statements.views import ORDER_COLUMNS_NAME, GoodSerializerPlus, GOOD_COLUMNS_NAME
from utils.list_pages import CustomDjangoFilterBackend, CusResponse, CustomExportListView
from ..utils import FreightStatementFilterSet, OrderStatementFilterSet, FreightQueryFilterSet
from ..serializers import FreightStatementSerial, FreightPandasSerializer, OrderStatementSerial

FREIGHT_COLUMNS_NAME = ['序号', '运单号', '货运公司', '中港公司', '运单状态',
                        '货运渠道', '运单时间', '中转站', '实收重量', '重量', '体积']


# 运单报表查询视图
class FreightReportQueryViews(ListAPIView):
    """运单报表查询视图"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = FreightQueryFilterSet
    pagination_class = CusResponse


# 运单报表导出视图
class FreightExportSingleViews(CustomExportListView):
    """运单报表导出视图"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = FreightQueryFilterSet

    excel_name = '运单查询报表.xlsx'
    sheet_names = ['运单']
    total_columns = ['price_w', 'weight', 'volume']
    columns_names = [FREIGHT_COLUMNS_NAME]


# 运单报表导出 两表单
class FreightExportPluralViews(CustomExportListView):
    """运单报表导出 两表单"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = FreightQueryFilterSet

    excel_name = '运单查询报表(订单).xlsx'
    sheet_names = ['运单', '订单']
    total_columns = ['price_w', 'weight', 'volume']
    sub__models = [OrdersInfo]
    sub_serializers = [OrderStatementSerial]
    columns_names = [FREIGHT_COLUMNS_NAME, ORDER_COLUMNS_NAME]


# 运单报表导出 三表单
class FreightExportPluralViewsPlus(FreightExportPluralViews):
    """运单报表导出 三表单"""

    excel_name = '运单查询报表(订单/货物).xlsx'
    sheet_names = ['运单', '订单', '货物']
    total_columns = ['price_w', 'weight', 'volume']
    sub__models = [OrdersInfo, GoodsInfo]
    sub_serializers = [OrderStatementSerial, GoodSerializerPlus]
    columns_names = [FREIGHT_COLUMNS_NAME, ORDER_COLUMNS_NAME, GOOD_COLUMNS_NAME]


# 运单报表查询视图(统计)
class FreightReportStatisticsQueryViews(ListAPIView):
    """运单报表查询视图"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderStatementFilterSet
    pagination_class = CusResponse


# 运单报表导出视图(统计)
class FreightReportStatisticsSingleViews(CustomExportListView):
    """运单报表导出视图(统计)"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderStatementFilterSet

    excel_name = '运单统计报表.xlsx'
    sheet_names = ['运单']
    total_columns = ['price_w', 'weight', 'volume']
    columns_names = [FREIGHT_COLUMNS_NAME]
    sub_total = True


# 运单报表导出视图(统计 两表单)
class FreightReportStatisticsPluralViews(CustomExportListView):
    """运单报表导出视图(统计 两表单)"""

    queryset = FreightsInfo.objects.prefetch_related(
        'channel', 'pay_type', 'trans_company', 'mid_company'
    ).all()
    serializer_class = FreightStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderStatementFilterSet

    excel_name = '运单统计报表(订单).xlsx'
    sheet_names = ['运单', '订单']
    total_columns = ['price_w', 'weight', 'volume']
    columns_names = [FREIGHT_COLUMNS_NAME, ORDER_COLUMNS_NAME]
    sub__models = [OrdersInfo]
    sub_serializers = [OrderStatementSerial]
    sub_total = True


# 运单报表导出视图(统计 三表单)
class FreightReportStatisticsPluralViewsPlus(FreightReportStatisticsPluralViews):
    """运单报表导出视图(统计 三表单)"""

    excel_name = '运单统计报表(订单/货物).xlsx'
    sheet_names = ['运单', '订单', '货物']
    columns_names = [FREIGHT_COLUMNS_NAME, ORDER_COLUMNS_NAME, GOOD_COLUMNS_NAME]
    sub__models = [OrdersInfo, GoodsInfo]
    sub_serializers = [OrderStatementSerial, GoodSerializerPlus]
    sub_total = True


if __name__ == '__main__':
    pass
