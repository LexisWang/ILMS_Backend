from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import CusChaPri


class ChaPriSerializer(serializers.ModelSerializer):
    """客户服务渠道价格反序列化器"""

    creator = serializers.StringRelatedField(read_only=True)
    modifier = serializers.SlugRelatedField(read_only=True, slug_field='username')
    create_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CusChaPri
        fields = [
            'owner_code',
            'channel_code',
            'channel_name',
            'unit_price',
            'insurance_rate',
            'creator',
            'modifier',
            'create_time',
            'modify_time',
        ]

    def create(self, validated_data):
        request_user = self.context.get('request').user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['creator'] = request_user
        validated_data['modifier'] = validated_data.get('creator')
        return super().create(validated_data)

    def update(self, instance, validated_data):

        request_user = self.context.get('request').user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['modifier'] = request_user
        return super().update(instance, validated_data)


if __name__ == '__main__':
    pass
