from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import OrdFundsInfo


class OrderFundSerializerAnti(serializers.ModelSerializer):
    """订单款项 序列化器"""

    class Meta:
        model = OrdFundsInfo
        fields = [
            'id',
            'order',
            'customer',
            'fund_status',
            'order_status',
            'pay_type',
            'channel',
            'service',
            'price_w',
            'insurance_rate',
            'y_account',
            's_account',
            'j_account',
            'w_account',
            'freight_fee',
            'dispatch_fee',
            'file_fee',
            'operate_fee',
            'insurance_fee',
            'server_fee',
            'insurance_money',
            'collection_money',
            'other_fee',
            'remark_comment',
            'attachment_ids',
            'order_time',
        ]
        extra_kwargs = {
            'id': {'help_text': '订单ID len <= 32'},
        }

    def create(self, validated_data):
        request_user = self.initial_data.get('request_user')
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['creator'] = request_user
        validated_data['modifier'] = validated_data.get('creator')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request_user = self.initial_data.get('request_user')
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['modifier'] = request_user
        return super().update(instance, validated_data)


class OrderFundSerializer(OrderFundSerializerAnti):
    fund_status = serializers.CharField(source='get_fund_status_display')
    order_status = serializers.CharField(source='get_order_status_display')
    order = serializers.StringRelatedField()
    customer = serializers.StringRelatedField()
    pay_type = serializers.StringRelatedField()
    channel = serializers.StringRelatedField()
    service = serializers.StringRelatedField()
    order_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    pass
