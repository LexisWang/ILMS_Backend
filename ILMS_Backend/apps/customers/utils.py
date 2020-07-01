from django_filters.rest_framework import FilterSet, filters

from systems.models import DataDictsValue, UsersInfo, Cities, Countries
from .models import CustomersInfo, ReceiversInfo


# 客户方过滤
class CustomersFilterSet(FilterSet):
    rank = filters.ModelChoiceFilter(queryset=DataDictsValue.objects.all(), help_text='用户级别')
    salesman = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='业务员')
    service = filters.ModelChoiceFilter(queryset=UsersInfo.objects.all(), help_text='专员')

    class Meta:
        model = CustomersInfo
        fields = []


# 收货方过滤
class ReceiversFilterSet(FilterSet):
    customer = filters.ModelChoiceFilter(queryset=CustomersInfo.objects.all(), required=True, help_text='客户代码')

    class Meta:
        model = ReceiversInfo
        fields = []


# 客户方检查
class CusCodeFilterSet(FilterSet):
    pk = filters.NumberFilter(help_text='id值')
    code = filters.CharFilter(help_text='代码')
    name = filters.CharFilter(help_text='名称')


# 收货方方检查
class RecCodeFilterSet(FilterSet):
    pk = filters.NumberFilter(help_text='id值')
    code = filters.CharFilter(help_text='代码')
    name = filters.CharFilter(help_text='名称')
    customer = filters.NumberFilter(help_text='国家')


class RecCityFilter(FilterSet):
    county = filters.ModelChoiceFilter(queryset=Countries.objects.all(), required=True, help_text='所属国家')

    class Meta:
        model = Cities
        fields = []


if __name__ == '__main__':
    pass
