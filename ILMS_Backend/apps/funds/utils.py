from django_filters.rest_framework import FilterSet, filters

import settings
from systems.models import DataDictsValue, UsersInfo
from .models import OrdFundsInfo, FreFundsInfo, CustomsFundsInfo, OtherFundsInfo


# 订单过滤
class OrdFundsFilterSet(FilterSet):
    fund_status = filters.ChoiceFilter(choices=settings.FUND_STATUS_CHOICE, help_text='款项状态')
    order_status = filters.ChoiceFilter(choices=settings.ORDER_STATUS_CHOICE, help_text='订单状态')
    channel = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='服务渠道')
    pay_type = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='付款类型')
    order_time_start = filters.DateTimeFilter(field_name='order_time', lookup_expr='gte', help_text='订单(查询起始时间)')
    order_time_end = filters.DateTimeFilter(field_name='order_time', lookup_expr='lte', help_text='订单(查询结束时间)')

    class Meta:
        model = OrdFundsInfo
        fields = []


# 运单过滤
class FreFundsFilterSet(FilterSet):
    fund_status = filters.ChoiceFilter(choices=settings.FUND_STATUS_CHOICE, help_text='款项状态')
    order_status = filters.ChoiceFilter(choices=settings.ORDER_STATUS_CHOICE, help_text='订单状态')
    channel = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='服务渠道')
    trans_company = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='货运公司')
    pack_time_start = filters.DateTimeFilter(field_name='pack_time', lookup_expr='gte', help_text='订单(查询起始时间)')
    pack_time_end = filters.DateTimeFilter(field_name='pack_time', lookup_expr='lte', help_text='订单(查询结束时间)')

    class Meta:
        model = FreFundsInfo
        fields = []


# 运单过滤
class CustomsFundsFilterSet(FilterSet):
    fund_status = filters.ChoiceFilter(choices=settings.FUND_STATUS_CHOICE, help_text='款项状态')
    channel = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='货运渠道')
    pack_time_start = filters.DateTimeFilter(field_name='pack_time', lookup_expr='gte', help_text='订单(查询起始时间)')
    pack_time_end = filters.DateTimeFilter(field_name='pack_time', lookup_expr='lte', help_text='订单(查询结束时间)')

    class Meta:
        model = CustomsFundsInfo
        fields = []


# 运单过滤
class OthersFundsFilterSet(FilterSet):
    fund_type = filters.ChoiceFilter(choices=settings.OTHER_FUND_TYPE_CHOICE, help_text='款项类型')
    fund_status = filters.ChoiceFilter(choices=settings.FUND_STATUS_CHOICE, help_text='款项状态')
    order = filters.ModelChoiceFilter(queryset=OrdFundsInfo.objects.all(), help_text='订单')
    freight = filters.ModelChoiceFilter(queryset=FreFundsInfo.objects.all(), help_text='运单')
    service = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='款项专员')
    recpay_time_start = filters.DateTimeFilter(field_name='recpay_time', lookup_expr='gte', help_text='订单(查询起始时间)')
    recpay_time_end = filters.DateTimeFilter(field_name='recpay_time', lookup_expr='lte', help_text='订单(查询结束时间)')

    class Meta:
        model = OtherFundsInfo
        fields = []
