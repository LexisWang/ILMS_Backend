from django_filters.rest_framework import FilterSet, filters

import settings
from systems.models import UsersInfo, DataDictsValue
from .models import OrdersInfo, FreightsInfo


# 订单过滤
class OrdersFilterSet(FilterSet):
    customer__salesman = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='业务员')
    customer__service = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='客服专员')
    operators = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='操作员')
    order_status = filters.ChoiceFilter(choices=settings.ORDER_STATUS_CHOICE, help_text='订单状态')
    channel = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='服务渠道')
    order_time_start = filters.DateTimeFilter(field_name='order_time', lookup_expr='order_time__gte', help_text='订单时间')
    order_time_end = filters.DateTimeFilter(field_name='order_time', lookup_expr='order_time_lte', help_text='订单时间')

    class Meta:
        model = OrdersInfo
        fields = []


# 订单选项过滤参数
class OrderOptionFilter(FilterSet):
    customer_code = filters.CharFilter(help_text='客户代码')


# 运单过滤
class FreightsFilterSet(FilterSet):
    channel = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='货运渠道')
    trans_company = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='货运公司')
    freight_status = filters.ChoiceFilter(choices=settings.FREIGHT_STATUS_CHOICE, help_text='货运状态')
    pack_time_start = filters.DateTimeFilter(field_name='pack_time', lookup_expr='gte', help_text='查询运单(起始打包时间)')
    pack_time_end = filters.DateTimeFilter(field_name='pack_time', lookup_expr='lte', help_text='查询运单(结束打包时间）')

    class Meta:
        model = FreightsInfo
        fields = []


# 运单选项过滤参数
class FreightTMOrdFilterSet(FilterSet):
    channel_code = filters.CharFilter(help_text='客户代码')
    freight = filters.NumberFilter(help_text='运单')


# 物流信息过滤参数
class LogisticFilterSet(FilterSet):
    order = filters.NumberFilter(help_text='订单')
    freight = filters.NumberFilter(help_text='运单')
