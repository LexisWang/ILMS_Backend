import copy
from datetime import datetime

import pytz
from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

import settings
from customers.models import CustomersInfo, ReceiversInfo
from funds.models import OrdFundsInfo
from funds.serializers import OrderFundSerializerAnti
from systems.models import CusChaPri, DataDictsValue, UsersInfo, Countries
from systems.serializers import CountySer
from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import OrdersInfo
from ..serializers import OrderSerializerAnti, OrderSerializer
from ..utils import OrdersFilterSet, OrderOptionFilter


# 订单读视图集
class OrderReadViews(ReadModelViewSetPlus):
    """订单读视图集"""

    queryset = OrdersInfo.objects.filter().all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = OrdersFilterSet
    pagination_class = CusResponse
    search_fields = ['trans_code']

    def get_queryset(self):
        return self._get_queryset(self.request.user, queryset=self.queryset, model=OrdersInfo)


# 订单写视图集
class OrderWriteViews(WriteModelViewSetPlus):
    """订单写视图集"""

    queryset = OrdersInfo.objects.filter().all()
    serializer_class = OrderSerializerAnti

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = copy.copy(request.data)
            data['request_user'] = self.request.user
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            order = serializer.instance  # type: OrdersInfo
            unit_price, insurance_rate = CusChaPri.objects.values_list('unit_price', 'insurance_rate').get(
                Q(owner_code=order.customer.code) & Q(channel_code=order.channel.code))
            _serializer = OrderFundSerializerAnti(data={
                'order': order.id,
                'order_status': order.order_status,
                'customer': order.customer_id,
                'pay_type': order.pay_type_id,
                'channel': order.channel_id,
                'insurance_rate': insurance_rate,
                'price_w': order.price_w,
                'collection_money': order.collection_money,
                'freight_fee': order.price_w * unit_price,
                'y_account': order.price_w * unit_price,
                'order_time': order.order_time,
                'request_user': self.request.user
            })
            _serializer.is_valid(raise_exception=True)
            _serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'message': '订单创建成功！', 'code': settings.SUCCESS_CODE, 'data': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            data = copy.copy(request.data)
            data['request_user'] = self.request.user
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            order = serializer.instance
            unit_price, insurance_rate = CusChaPri.objects.values_list('unit_price', 'insurance_rate').get(
                Q(owner_code=order.customer.code) & Q(channel_code=order.channel.code))
            now_time = datetime.today()
            data = {
                'order_status': order.order_status,
                'customer': order.customer_id,
                'pay_type': order.pay_type_id,
                'channel': order.channel_id,
                'insurance_rate': insurance_rate,
                'price_w': order.price_w,
                'collection_money': order.collection_money,
                'freight_fee': order.price_w * unit_price,
                'y_account': order.price_w * unit_price,
                'order_time': order.order_time,
                'modifier': self.request.user,
                'modify_time': datetime(year=now_time.year, month=now_time.month, day=now_time.day, hour=now_time.hour,
                                        minute=now_time.minute, second=now_time.second,
                                        tzinfo=pytz.timezone('Asia/Shanghai')),
            }
            OrdFundsInfo.objects.filter(order=instance).update(**data)
        return Response({'success': True, 'message': '订单修改成功！', 'code': settings.SUCCESS_CODE, 'data': serializer.data})


# 新增订单前提(获取客户列表)
class CustomersListView(GenericAPIView):
    """新增订单前提(获取客户列表)"""

    queryset = CustomersInfo.objects.all()

    def get(self, request, *args, **kwargs):
        return CusResponse.get_response(data=self.queryset.values('id', 'code', 'name'), message='获取客户列表成功')


# 新增订单前提(根据客户获取各种下拉选项列表)
class OrderOptionView(GenericAPIView):
    """新增订单前提(根据客户获取各种下拉选项列表)"""

    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderOptionFilter

    def get(self, request, *args, **kwargs):
        customer_code = self.request.query_params.get('customer_code')
        return CusResponse.get_response(data={
            'channels': CusChaPri.objects.values('id', 'channel_code', 'channel_name').filter(owner_code=customer_code),
            'pay_types': DataDictsValue.objects.values('id', 'code', 'name').filter(type__name=settings.PAY_TYPES, status=1),
            'good_types': DataDictsValue.objects.values('id', 'code', 'name').filter(type__code=settings.GOOD_TYPES, status=1),
            'salesman': UsersInfo.objects.values('id', 'account', 'username').filter(~Q(id=1) & Q(status=1)).order_by('-date_joined'),
            'receivers': ReceiversInfo.objects.values('id', 'code', 'name').filter(customer__code=customer_code),
            'tran_site': CountySer(Countries.objects.all(), many=True).data
        })


if __name__ == '__main__':
    pass
