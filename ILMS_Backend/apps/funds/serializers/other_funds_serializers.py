import time

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import OtherFundsInfo


class OthFundsSerializerAnti(serializers.ModelSerializer):
    """其他款项系列化"""

    class Meta:
        model = OtherFundsInfo
        fields = [
            'id',
            'fund_code',
            'fund_type',
            'fund_status',
            'order',
            'freight',
            'service',
            'payee_payer',
            'connect_ways',
            'y_account',
            's_account',
            'remark_comment',
            'attachment_ids',
            'recpay_time',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['fund_code'] = time.time_ns()
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


class OthFundsSerializer(OthFundsSerializerAnti):
    fund_status = serializers.CharField(source='get_fund_status_display')
    order = serializers.StringRelatedField()
    freight = serializers.StringRelatedField()
    service = serializers.StringRelatedField()
    recpay_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    pass
