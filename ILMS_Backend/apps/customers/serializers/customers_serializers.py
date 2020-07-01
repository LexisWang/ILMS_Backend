from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import CustomersInfo


class CusCreUpdSerAnti(serializers.ModelSerializer):
    """ 客户方信息反序列化器 """

    creator = serializers.StringRelatedField(read_only=True)
    modifier = serializers.SlugRelatedField(read_only=True, slug_field='username')
    create_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CustomersInfo
        fields = [
            'id',
            'code',
            'name',
            'rank',
            'salesman',
            'service',
            'president_name',
            'connect_ways',
            'customer_address',
            'manage_directions',
            'remark_comment',
            'attachment_ids',
            'creator',
            'modifier',
            'create_time',
            'modify_time',
        ]
        extra_kwargs = {
            'id': {'help_text': '业务ID', 'read_only': True},
        }

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


class CusCreUpdSer(CusCreUpdSerAnti):
    """客户方信息序列化器"""

    salesman = serializers.StringRelatedField(read_only=True)
    service = serializers.StringRelatedField(read_only=True)
    rank = serializers.StringRelatedField(read_only=True)


if __name__ == '__main__':
    pass
