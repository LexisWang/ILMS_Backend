from django.utils.encoding import escape_uri_path
from rest_framework.generics import ListAPIView
from rest_pandas import PandasView, PandasExcelRenderer

from business.models import OrdersInfo
from utils.list_pages import CusResponse, CustomDjangoFilterBackend
from ..utils import OrderStatementFilterSet
from ..serializers import OrderPandasSerializer, OrderStatementSerial


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
    filterset_class = OrderStatementFilterSet
    pagination_class = CusResponse


# 订单报表导出视图
class OrderPandasViews(PandasView):
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
    filterset_class = OrderStatementFilterSet

    pandas_serializer_class = OrderPandasSerializer
    renderer_classes = [PandasExcelRenderer]

    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            return escape_uri_path("订单报表(查询)")
        else:
            return None


if __name__ == '__main__':
    pass
