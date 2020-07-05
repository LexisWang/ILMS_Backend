from rest_framework.generics import ListAPIView

from business.models import OrdersInfo, GoodsInfo
from business.serializers.goods_serializers import GoodSerializerPlus
from utils.list_pages import CusResponse, CustomDjangoFilterBackend, CustomExportListView
from ..utils import OrderStatementFilterSet, OrderQueryFilterSet
from ..serializers import OrderStatementSerial


ORDER_COLUMNS_NAME = ['序号', '转单号', '所属客户', '货物名称', '货物品名', '货物类型', '订单状态', '所属渠道',
                      '业务员', '客服专员', '操作员', '目的地', '收货方', '订单时间', '价格重量', '重量', '体积']
GOOD_COLUMNS_NAME = ['序号', '是否真实数据', '所属订单号', '货物名称', '重量', '货物件数', '货物数量',
                     '货物长', '货物宽', '货物高', '货物体积', '申报价格', 'SKU名称', '海关编码']


# 订单报表查询视图
class OrderReportQueryViews(ListAPIView):
    """订单报表查询视图"""

    queryset = OrdersInfo.objects.prefetch_related(
        'freight', 'customer', 'channel', 'good_type',
        'pay_type', 'operators', 'receiver'
    ).extra(
        select={
            'salesman': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on salesman_id = c.id
                """,
            'service': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on service_id = c.id
                """
        }
    ).all()
    serializer_class = OrderStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderQueryFilterSet
    pagination_class = CusResponse


# 订单报表导出视图
class OrderExportSingleViews(CustomExportListView):
    """订单报表导出视图"""

    queryset = OrdersInfo.objects.prefetch_related(
        'freight', 'customer', 'channel', 'good_type',
        'pay_type', 'operators', 'receiver'
    ).extra(
        select={
            'salesman': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on salesman_id = c.id
                """,
            'service': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on service_id = c.id
                """
        }
    ).all()
    serializer_class = OrderStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderQueryFilterSet

    excel_name = '订单查询报表.xlsx'
    sheet_names = ['订单']
    total_columns = ['price_w', 'weight', 'volume']
    columns_names = [ORDER_COLUMNS_NAME]


# 订单报表导出多表单
class OrderExportPluralViews(CustomExportListView):
    """订单报表导出多表单"""

    queryset = OrdersInfo.objects.prefetch_related(
        'freight', 'customer', 'channel', 'good_type',
        'pay_type', 'operators', 'receiver'
    ).extra(
        select={
            'salesman': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on salesman_id = c.id
                """,
            'service': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on service_id = c.id
                """
        }
    ).all()
    serializer_class = OrderStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderQueryFilterSet

    excel_name = '订单查询报表(货物).xlsx'
    sheet_names = ['订单', '货物']
    total_columns = ['price_w', 'weight', 'volume']
    sub__models = [GoodsInfo]
    sub_serializers = [GoodSerializerPlus]
    columns_names = [ORDER_COLUMNS_NAME, GOOD_COLUMNS_NAME]
    
    
# 订单报表查询视图(统计)
class OrderReportStatisticsQueryViews(ListAPIView):
    """订单报表查询视图(统计)"""

    queryset = OrdersInfo.objects.prefetch_related(
        'freight', 'customer', 'channel', 'good_type',
        'pay_type', 'operators', 'receiver'
    ).extra(
        select={
            'salesman': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on salesman_id = c.id
                """,
            'service': """
                    select c.username
                    from b_orders a
                             inner join i_customers b on a.customer_id = b.id
                             inner join s_users c on service_id = c.id
                """
        }
    ).all()
    serializer_class = OrderStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderStatementFilterSet
    pagination_class = CusResponse


# 订单报表导出视图(统计)
class OrderReportStatisticsSingleViews(CustomExportListView):
    """订单报表导出视图(统计)"""

    queryset = OrdersInfo.objects.prefetch_related(
        'freight', 'customer', 'channel', 'good_type',
        'pay_type', 'operators', 'receiver'
    ).extra(
        select={
            'salesman': """
                        select c.username
                        from b_orders a
                                 inner join i_customers b on a.customer_id = b.id
                                 inner join s_users c on salesman_id = c.id
                    """,
            'service': """
                        select c.username
                        from b_orders a
                                 inner join i_customers b on a.customer_id = b.id
                                 inner join s_users c on service_id = c.id
                    """
        }
    ).all()
    serializer_class = OrderStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderStatementFilterSet

    excel_name = '订单统计报表.xlsx'
    sheet_names = ['订单']
    total_columns = ['price_w', 'weight', 'volume']
    columns_names = [ORDER_COLUMNS_NAME]
    sub_total = True


# 订单报表导出视图(统计 多表单)
class OrderReportStatisticsPluralViews(CustomExportListView):
    """订单报表导出视图(统计 多表单)"""

    queryset = OrdersInfo.objects.prefetch_related(
        'freight', 'customer', 'channel', 'good_type',
        'pay_type', 'operators', 'receiver'
    ).extra(
        select={
            'salesman': """
                        select c.username
                        from b_orders a
                                 inner join i_customers b on a.customer_id = b.id
                                 inner join s_users c on salesman_id = c.id
                    """,
            'service': """
                        select c.username
                        from b_orders a
                                 inner join i_customers b on a.customer_id = b.id
                                 inner join s_users c on service_id = c.id
                    """
        }
    ).all()
    serializer_class = OrderStatementSerial
    filter_backends = [CustomDjangoFilterBackend]
    filterset_class = OrderStatementFilterSet

    excel_name = '订单统计报表(货物).xlsx'
    sheet_names = ['订单', '货物']
    total_columns = ['price_w', 'weight', 'volume']
    columns_names = [ORDER_COLUMNS_NAME, GOOD_COLUMNS_NAME]
    sub__models = [GoodsInfo]
    sub_serializers = [GoodSerializerPlus]
    sub_total = True


if __name__ == '__main__':
    pass
