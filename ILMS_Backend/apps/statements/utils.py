from django_filters.rest_framework import FilterSet, filters

import settings
from business.models import OrdersInfo, FreightsInfo
from systems.models import DataDictsValue, UsersInfo
from customers.models import CustomersInfo


# 订单报表过滤
class OrderStatementFilterSet(FilterSet):
    trans_code = filters.CharFilter(field_name='trans_code', lookup_expr='iexact', help_text='转单号', label='转单号')
    customer = filters.ModelChoiceFilter(queryset=CustomersInfo.objects.all(), help_text='客户', label='客户')
    order_status = filters.ChoiceFilter(choices=settings.ORDER_STATUS_CHOICE, help_text='订单状态', label='订单状态')
    channel = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='服务渠道', label='服务渠道')
    order_time_start = filters.DateTimeFilter(field_name='order_time', lookup_expr='gte', label='订单时间')
    order_time_end = filters.DateTimeFilter(field_name='order_time', lookup_expr='lte', label='订单时间')
    customer__salesman = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='业务员')
    customer__service = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='客服专员')
    operators = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='操作员', label='操作员')

    class Meta:
        model = OrdersInfo
        fields = []


# 运单报表过滤
class FreightStatementFilterSet(FilterSet):
    freight_code = filters.CharFilter(field_name='trans_code', lookup_expr='iexact', help_text='运单号', label='运单号')
    trans_company = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='货运公司', label='货运公司')
    mid_company = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='中港公司', label='中港公司')
    freight_status = filters.ChoiceFilter(choices=settings.ORDER_STATUS_CHOICE, help_text='运单状态', label='运单状态')
    channel = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='货运渠道', label='货运渠道')
    pack_time_start = filters.DateTimeFilter(field_name='pack_time', lookup_expr='gte', help_text='运单时间', label='运单时间')
    pack_time_end = filters.DateTimeFilter(field_name='pack_time', lookup_expr='lte', help_text='运单时间', label='运单时间')

    class Meta:
        model = FreightsInfo
        fields = []


if __name__ == '__main__':
    pass
