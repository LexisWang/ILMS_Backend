from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import GoodsInfo


class GoodSerializer(serializers.ModelSerializer):
    """货物序列化器"""

    class Meta:
        model = GoodsInfo
        fields = [
            'type',
            'order',
            'name',
            'weight',
            'kits',
            'number',
            'length',
            'width',
            'height',
            'volume',
            'declared_price',
            'sku_name',
            'customs_code',
        ]

    def create(self, validated_data):
        request_user = self.initial_data[0].get('request_user')
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['creator'] = request_user
        validated_data['modifier'] = validated_data.get('creator')
        return super().create(validated_data)


if __name__ == '__main__':
    pass
