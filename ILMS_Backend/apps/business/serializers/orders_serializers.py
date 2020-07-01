from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from rest_framework import serializers

from systems.models import UsersInfo
from .goods_serializers import GoodSerializer, GoodSerializerPlus
from ..models import OrdersInfo, Order2Operator, GoodsInfo


class OrderSerializerAnti(serializers.ModelSerializer):
    """订单序反列化器"""

    goods = GoodSerializer(many=True)
    operators = serializers.ManyRelatedField(
        child_relation=serializers.PrimaryKeyRelatedField(label='所属角色', help_text='订单关联的操作员',
                                                          queryset=UsersInfo.objects.all()), help_text='用户关联的角色',
        required=False, label='所属角色')

    class Meta:
        model = OrdersInfo
        fields = [
            'id',
            'trans_code',
            'order_status',
            'freight',
            'customer',
            'channel',
            'good_type',
            'pay_type',
            'operators',
            'collection_money',
            'v_w_rate',
            'volume',
            'volume_w',
            'weight',
            'price_w',
            'number',
            'transport_site',
            'goods_name',
            'goods_name_en',
            'flight_number',
            'remark_comment',
            'order_time',
            'receiver',
            'goods',
        ]
        extra_kwargs = {
            'id': {'help_text': '订单号', 'read_only': True},
        }

    def create(self, validated_data):
        request_user = self.initial_data.get('request_user')
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['creator'] = request_user
        validated_data['modifier'] = validated_data.get('creator')

        goods = validated_data.pop('goods')
        operators = validated_data.pop('operators')
        with transaction.atomic():
            order = OrdersInfo.objects.create(**validated_data)
            order.operators.set(operators)
            for good in goods:
                good['order_id'] = order.id
                good['request_user'] = request_user
            serializer = GoodSerializer(data=goods, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            order.goods.set(serializer.instance)
            order.save()
        return order

    def update(self, instance, validated_data):
        with transaction.atomic():
            request_user = self.initial_data.get('request_user')
            if isinstance(request_user, AnonymousUser):
                request_user = None
            validated_data['modifier'] = request_user

            GoodsInfo.objects.filter(order=instance).delete()
            Order2Operator.objects.filter(order=instance).delete()
            goods = validated_data.pop('goods')
            operators = validated_data.pop('operators')

            with transaction.atomic():
                OrdersInfo.objects.filter(id=instance.id).update(**validated_data)
                order = OrdersInfo.objects.get(id=instance.id)
                order.operators.set(operators)
                for good in goods:
                    good['order_id'] = order.id
                    good['request_user'] = request_user
                serializer = GoodSerializer(data=goods, many=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                order.goods.set(serializer.instance)
                order.save()
            return order


class OrderSerializer(OrderSerializerAnti):
    """订单序列化器"""

    order_status = serializers.CharField(source='get_order_status_display')
    freight = serializers.StringRelatedField()
    customer = serializers.StringRelatedField()
    channel = serializers.StringRelatedField()
    good_type = serializers.StringRelatedField()
    pay_type = serializers.StringRelatedField()
    operators = serializers.StringRelatedField(many=True)
    receiver = serializers.StringRelatedField()
    order_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    goods = GoodSerializerPlus(many=True)


if __name__ == '__main__':
    pass
