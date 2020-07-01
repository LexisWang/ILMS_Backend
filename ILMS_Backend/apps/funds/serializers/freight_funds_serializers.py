from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import FreFundsInfo


class FreFundsSerializerAnti(serializers.ModelSerializer):
    """货运款项序列化器"""

    class Meta:
        model = FreFundsInfo
        fields = [
            'id',
            'freight',
            'fund_status',
            'freight_status',
            'pay_type',
            'trans_company',
            'mid_company',
            'channel',
            'service',
            'price_w',
            'y_account',
            's_account',
            'j_account',
            'w_account',
            'freight_fee',
            'lading_fee',
            'magntest_fee',
            'operate_fee',
            'file_fee',
            'custclea_fee',
            'collection_money',
            'other_fee',
            'remark_comment',
            'attachment_ids',
            'pack_time',
        ]
        extra_kwargs = {
            'id': {'help_text': 'ID', 'read_only': True},
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


class FreFundsSerializer(FreFundsSerializerAnti):
    fund_status = serializers.CharField(source='get_fund_status_display')
    freight_status = serializers.CharField(source='get_freight_status_display')
    freight = serializers.StringRelatedField()
    pay_type = serializers.StringRelatedField()
    trans_company = serializers.StringRelatedField()
    mid_company = serializers.StringRelatedField()
    channel = serializers.StringRelatedField()
    service = serializers.StringRelatedField()
    pack_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    pass
