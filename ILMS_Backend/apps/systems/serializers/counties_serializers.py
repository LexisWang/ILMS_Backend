from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from .cities_serializers import CitySer
from ..models import Countries


class CountySerializer(serializers.ModelSerializer):
    """国家序列化器"""

    creator = serializers.StringRelatedField(read_only=True)
    modifier = serializers.SlugRelatedField(read_only=True, slug_field='username')
    create_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Countries
        fields = [
            'id',
            'code',
            'name',
            'creator',
            'modifier',
            'create_time',
            'modify_time',
        ]
        extra_kwargs = {
            'id': {'help_text': '业务ID len <= 32', 'read_only': True},
            'code': {'help_text': '国家代码 len <= 64'},
            'name': {'help_text': '国家名称 len <= 100'}
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


class CountySer(serializers.ModelSerializer):
    cities = CitySer(many=True)

    class Meta:
        model = Countries
        fields = ['id', 'code', 'name', 'cities']


if __name__ == '__main__':
    pass
