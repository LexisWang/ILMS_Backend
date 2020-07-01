import time

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from rest_framework import serializers

from funds.models import OrdFundsInfo
from ..models import FreightsInfo, OrdersInfo


class FreightSerializerAnti(serializers.ModelSerializer):
    """运单序反列化器"""

    class Meta:
        model = FreightsInfo
        fields = [
            'id',
            'freight_code',
            'freight_status',
            'channel',
            'pay_type',
            'trans_company',
            'mid_company',
            'kits',
            'weight',
            'volume',
            'price_w',
            'volume_w',
            'collection_money',
            'transport_site',
            'order_codes',
            'mid_port',
            'flight_number',
            'remark_comment',
            'pack_time',
        ]
        extra_kwargs = {
            'id': {'help_text': '运单号', 'read_only': True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['freight_code'] = time.time_ns()
            request_user = self.initial_data.get('request_user')
            if isinstance(request_user, AnonymousUser):
                request_user = None
            validated_data['creator'] = request_user
            validated_data['modifier'] = validated_data.get('creator')
            freight = super().create(validated_data)
            # 获取相关的订单(更新订单和订单款项)
            orders = OrdersInfo.objects.filter(id__in=validated_data.get('order_codes'))
            orders.update(freight=freight, order_status=2)
            OrdFundsInfo.objects.filter(order__in=orders).update(order_status=2)
        return freight

    def update(self, instance, validated_data):
        request_user = self.initial_data.get('request_user')
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['modifier'] = request_user
        # 获取相关的订单(更新订单和订单款项)
        orders = OrdersInfo.objects.filter(freight=instance)
        orders.update(freight_code=None, order_status=1)
        OrdFundsInfo.objects.filter(order__in=orders).update(order_status=1)
        OrdersInfo.objects.filter(id__in=validated_data.get('order_codes')).update(freight=instance, order_status=2)
        # 更新运单
        return super(FreightSerializerAnti, self).update(instance, validated_data)


class FreightSerializer(FreightSerializerAnti):
    """运单序列化器"""

    freight_status = serializers.CharField(source='get_freight_status_display')
    channel = serializers.StringRelatedField()
    pay_type = serializers.StringRelatedField()
    trans_company = serializers.StringRelatedField()
    mid_company = serializers.StringRelatedField()
    pack_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    pass
