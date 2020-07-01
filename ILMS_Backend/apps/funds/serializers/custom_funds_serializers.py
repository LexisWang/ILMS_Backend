from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import CustomsFundsInfo


class CustomsFundSerialAnti(serializers.ModelSerializer):
    """清关款项序列化器"""

    class Meta:
        model = CustomsFundsInfo
        fields = [
            'id',
            'type',
            'freight',
            'fund_status',
            'channel',
            'service',
            'y_account',
            's_account',
            'j_account',
            'w_account',
            'customs_fee',
            'remark_comment',
            'attachment_ids',
            'pack_time',
        ]
        extra_kwargs = {
            'id': {'read_only': True, 'help_text': 'ID'},
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


class CustomsFundSerial(CustomsFundSerialAnti):
    fund_status = serializers.CharField(source='get_fund_status_display')
    freight = serializers.StringRelatedField()
    channel = serializers.StringRelatedField()
    service = serializers.StringRelatedField()
    pack_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    pass
