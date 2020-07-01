from django_filters.rest_framework import FilterSet, filters

import settings
from .models import BranchesInfo, RolesInfo, UsersInfo, DataDictsValue, DataDictType, Cities, CusChaPri, Countries


# 分部集过滤条件
class BranchFilterSet(FilterSet):
    status = filters.ChoiceFilter(choices=settings.STATUS_USE_CHOICE, label='状态是否启动')

    class Meta:
        model = BranchesInfo
        fields = []


# 角色集过滤条件
class RoleFilterSet(FilterSet):
    status = filters.ChoiceFilter(choices=settings.STATUS_USE_CHOICE, help_text='状态是否启动')
    data_level = filters.ChoiceFilter(choices=settings.DATA_LEVEL_CHOICE, help_text='数据级别')

    class Meta:
        model = RolesInfo
        fields = []


# 用户集过滤条件
class UserFilterSet(FilterSet):
    status = filters.ChoiceFilter(choices=settings.STATUS_USE_CHOICE, help_text='状态是否启动')
    bran = filters.ModelChoiceFilter(queryset=BranchesInfo.objects.all(), help_text='分部id')
    roles = filters.ModelChoiceFilter(queryset=RolesInfo.objects.all(), label='角色ID')

    class Meta:
        model = UsersInfo
        fields = []


# 检查角色名称
class CheckRoleNameFilter(FilterSet):
    pk = filters.NumberFilter(help_text='id值')
    name = filters.CharFilter(help_text='角色名称')


# 检查分部名称
class CheckBranNameFilter(FilterSet):
    pk = filters.NumberFilter(help_text='id值')
    name = filters.CharFilter(help_text='分部名称')


# 检查账号
class CheckUserAccFilter(FilterSet):
    pk = filters.NumberFilter(help_text='id值')
    account = filters.CharFilter(help_text='账号')


# 检查用户名
class CheckUserNameFilter(FilterSet):
    pk = filters.NumberFilter(help_text='id值')
    username = filters.CharFilter(help_text='用户名')


# 检查类型(国家)
class CheckTypeFilter(FilterSet):
    pk = filters.NumberFilter(help_text='业务pk')
    code = filters.CharFilter(help_text='类型代码')
    name = filters.CharFilter(help_text='类型名称')


# 检查字典值
class CheckValueFilter(FilterSet):
    pk = filters.NumberFilter(help_text='业务id')
    code = filters.CharFilter(help_text='代码')
    name = filters.CharFilter(help_text='名称')
    type = filters.ModelChoiceFilter(queryset=DataDictType.objects.all(), required=True, help_text='类型')

    class Meta:
        model = DataDictsValue
        fields = []


# 检查城市
class CityFilter(FilterSet):
    pk = filters.NumberFilter(help_text='业务id')
    code = filters.CharFilter(help_text='代码')
    name = filters.CharFilter(help_text='名称')
    county = filters.ModelChoiceFilter(queryset=Countries.objects.all(), required=True, help_text='国家')

    class Meta:
        model = Cities
        fields = []


# 字典值过滤
class DictValuesFilterSet(FilterSet):
    type = filters.ModelChoiceFilter(queryset=DataDictType.objects.all(), required=True, help_text='字典类型代码')
    status = filters.ChoiceFilter(choices=settings.STATUS_USE_CHOICE, label='状态是否启动')

    class Meta:
        model = DataDictsValue
        fields = []


# 城市过滤
class CitiesFilterSet(FilterSet):
    county = filters.ModelChoiceFilter(queryset=Countries.objects.all(), required=True, help_text='国家')
    status = filters.ChoiceFilter(choices=settings.STATUS_USE_CHOICE, label='状态是否启动')

    class Meta:
        model = Cities
        fields = []


# 价格配置过滤
class PricesFilterSet(FilterSet):
    owner_code = filters.CharFilter(field_name='owner_code', lookup_expr='iexact', help_text='所属者')

    class Meta:
        model = CusChaPri
        fields = []


if __name__ == '__main__':
    pass
