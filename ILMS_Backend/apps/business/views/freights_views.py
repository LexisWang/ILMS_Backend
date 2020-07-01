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
from funds.models import FreFundsInfo, CustomsFundsInfo
from funds.serializers import FreFundsSerializerAnti, CustomsFundSerialAnti
from systems.models import CusChaPri, DataDictsValue, DataDictType, Countries
from systems.serializers import CountySer
from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from utils.raw_sql import RawSQL
from ..models import FreightsInfo, OrdersInfo
from ..serializers import FreightSerializerAnti, FreightSerializer
from ..utils import FreightsFilterSet, FreightTMOrdFilterSet


# 运单读视图集
class FreightReadViews(ReadModelViewSetPlus):
    """运单读视图集"""

    queryset = FreightsInfo.objects.all()
    serializer_class = FreightSerializer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = FreightsFilterSet
    pagination_class = CusResponse
    search_fields = ['freight_code']

    def get_queryset(self):
        return self._get_queryset(self.request.user, queryset=self.queryset, model=FreightsInfo)


# 运单写视图集
class FreightWriteViews(WriteModelViewSetPlus):
    """运单写视图集"""

    queryset = FreightsInfo.objects.all()
    serializer_class = FreightSerializerAnti

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = copy.copy(request.data)
            data['request_user'] = self.request.user
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # 创建运单款项
            freight = serializer.instance  # type: FreightsInfo
            unit_price = CusChaPri.objects.values_list('unit_price', flat=True).get(
                Q(owner_code=freight.trans_company.code) & Q(channel_code=freight.channel.code))
            _serializer = FreFundsSerializerAnti(data={
                'freight': freight.id,
                'freight_status': freight.freight_status,
                'pay_type': freight.pay_type_id,
                'trans_company': freight.trans_company_id,
                'channel': freight.channel_id,
                'price_w': freight.price_w,
                'collection_money': freight.collection_money,
                'freight_fee': freight.price_w * unit_price,
                'y_account': freight.price_w * unit_price,
                'pack_time': freight.pack_time,
                'request_user': self.request.user
            })
            _serializer.is_valid(raise_exception=True)
            _serializer.save()

            # 创建中港款项
            if data.get('mid_company'):
                unit_price_ = CusChaPri.objects.values_list('unit_price', flat=True).get(
                    Q(owner_code=freight.mid_company.code) & Q(channel_code=freight.channel.code))
                data_ = copy.deepcopy(data)
                data_['freight_fee'] = data_.get('price_w') * unit_price_
                data_['y_account'] = data_.get('freight_fee')
                data_['trans_company'] = None
            else:
                data_ = None

            data['mid_company'] = None
            serializer = FreFundsSerializerAnti(data=[data, data_], many=True)
            serializer.is_valid()
            serializer.save()

            # 添加清关款项两个
            data0 = copy.deepcopy(data)
            data0['type'] = 0
            data1 = copy.deepcopy(data)
            data1['type'] = 1

            # 计算清关费
            try:
                _unit_price = CusChaPri.objects.values_list('unit_price', flat=True).get(
                    Q(owner_code=settings.CUSTOMS) & Q(channel_code=freight.channel.code))
            except Exception as e:
                _unit_price = 0
            data1['customs_fee'] = data1.get('price_w') * _unit_price
            data1['y_account'] = data1.get('customs_fee')
            data0['y_account'] = 0
            data1['fund_status'] = 2  # 把业务级的清关款项设置为‘待结算’

            serializer0 = CustomsFundSerialAnti(data=[data0, data1], many=True)
            serializer0.is_valid()
            serializer0.save()
            headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'message': '运单创建成功！', 'code': settings.SUCCESS_CODE, 'data': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = copy.copy(request.data)
        data['request_user'] = self.request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()  # type: FreightsInfo
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # 修改运单款项
        freight = serializer.instance  # type: FreightsInfo
        unit_price = CusChaPri.objects.values_list('unit_price', flat=True).get(
            Q(owner_code=freight.trans_company.code) & Q(channel_code=freight.channel.code))
        now_time = datetime.today()
        data = {
            'freight_status': freight.freight_status,
            'pay_type': freight.pay_type_id,
            'trans_company': freight.trans_company_id,
            'channel': freight.channel_id,
            'price_w': freight.price_w,
            'collection_money': freight.collection_money,
            'freight_fee': freight.price_w * unit_price,
            'y_account': freight.price_w * unit_price,
            'pack_time': freight.pack_time,
            'request_user': self.request.user,
            'modify_time': datetime(year=now_time.year, month=now_time.month, day=now_time.day, hour=now_time.hour,
                                    minute=now_time.minute, second=now_time.second,
                                    tzinfo=pytz.timezone('Asia/Shanghai')),
        }
        FreFundsInfo.objects.filter(freight=freight).update(**data)

        if data.get('mid_company') and FreFundsInfo.objects.filter(freight=freight).count() == 2:
            unit_price_ = CusChaPri.objects.values_list('unit_price', flat=True).get(
                Q(owner_code=freight.mid_company.code) & Q(channel_code=freight.channel.code))
            data_ = copy.deepcopy(data)
            data_['freight_fee'] = data_.get('price_w') * unit_price_
            data_['y_account'] = data_.get('freight_fee')
            data_['trans_company'] = None
            old_freight_fee = FreFundsInfo.objects.get(freight=freight, trans_company__isnull=True).freight_fee
            if data_.get('freight_fee') != old_freight_fee:
                data['fund_status'] = 1
            FreFundsInfo.objects.filter(freight=freight, trans_company__isnull=True).update(**data_)
        elif data.get('mid_company') and FreFundsInfo.objects.filter(freight=freight).count() < 2:
            unit_price_ = CusChaPri.objects.values_list('unit_price', flat=True).get(
                Q(owner_code=freight.mid_company.code) & Q(channel_code=freight.channel.code))
            data_ = copy.deepcopy(data)
            data_['freight_fee'] = data_.get('price_w') * unit_price_
            data_['trans_company'] = None
            serializer = FreFundsSerializerAnti(data=data_)
            serializer.is_valid()
            serializer.save()
        elif not data.get('mid_company') and FreFundsInfo.objects.filter(freight=freight).count() == 2:
            FreFundsInfo.objects.get(freight=freight, trans_company__isnull=True).delete()
        data['mid_company'] = None
        FreFundsInfo.objects.filter(freight=freight, mid_company__isnull=True).update(**data)

        # 修改清关款项两个
        if freight.channel != instance.channel:
            data0 = copy.deepcopy(data)
            data1 = copy.deepcopy(data)
            # 计算清关费
            try:
                _unit_price = CusChaPri.objects.values_list('unit_price', flat=True).get(
                    Q(customer_code=settings.CUSTOMS) & Q(channel_code=freight.channel.code))
            except Exception:
                _unit_price = 0
            data1['customs_fee'] = data1.get('price_w') * _unit_price
            data1['y_account'] = data1.get('customs_fee')
            data0['y_account'] = 0
            data1['fund_status'] = 2  # 把业务级的清关款项设置为‘待结算’
            CustomsFundsInfo.objects.filter(freight=freight, type=0).update(**data0)
            CustomsFundsInfo.objects.filter(freight=freight, type=1).update(**data1)
        else:
            return super().update(instance, data)


# 新增运单前提(获取除 '货运公司','中港公司','可选订单' 各种下拉选项列表)
class FreightOptionView(GenericAPIView):
    """新增运单前提(获取除 '货运公司','中港公司','可选订单' 各种下拉选项列表)"""

    queryset = FreightsInfo.objects.all()

    def get(self, request, *args, **kwargs):
        return CusResponse.get_response(data={
            'channels': RawSQL(sql="""
                select a.id, b.code, b.name
                from s_price a  
                         inner join s_values b on a.channel_code = b.code
                         inner join s_types c on b.type_id = c.id
                where c.code = %s
                  and b.status = 1
                  and a.insurance_rate is null
                  and a.unit_price is not null
            """, params=[settings.TRANS_COMP]).dict_fetchall(),
            'pay_types': DataDictsValue.objects.values('id', 'code', 'name').filter(
                type=DataDictType.objects.get(code=settings.PAY_TYPES).id, status=1),
            'tran_site': CountySer(Countries.objects.all(), many=True).data
        })


# 新增运单前提(获取 '货运公司','中港公司','可选订单' 下拉选项列表)
class FreightTMOrdView(GenericAPIView):
    """新增运单前提(获取 '货运公司','中港公司','可选订单' 下拉选项列表)"""

    queryset = OrdersInfo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FreightTMOrdFilterSet

    def get(self, request, *args, **kwargs):
        channel_code = self.request.query_params.get('channel_code')
        freight = self.request.query_params.get('freight')
        channel = DataDictsValue.objects.get(code=channel_code)
        return CusResponse.get_response(data={
            'trans_company': RawSQL(sql="""
                select a.id, b.code, b.name
                from s_price a
                         left join s_values b on a.owner_code = b.code
                         left join s_types c on b.type_id = c.id
                where c.code = %s
                  and b.status = 1
                  and a.channel_code = %s
            """, params=[settings.TRANS_COMP, channel]).dict_fetchall(),
            'select_orders': self.queryset.filter(channel=channel, freight__isnull=True) \
                if not freight \
                else self.queryset.filter(Q(channel=channel) & (Q(freight__isnull=True) & Q(freight=freight)))
        })


if __name__ == '__main__':
    pass
