from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import RolesInfo


class RolesSerializerAnti(serializers.ModelSerializer):
    """角色序列反化器"""

    creator = serializers.StringRelatedField(read_only=True)
    modifier = serializers.SlugRelatedField(read_only=True, slug_field='username')
    create_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = RolesInfo
        fields = [
            'id',
            'name',
            'desc',
            'status',
            'level',
            'menu_list',
            'creator',
            'modifier',
            'create_time',
            'modify_time',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
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


class RolesSerializer(RolesSerializerAnti):
    """角色序列化器"""

    status = serializers.CharField(source='get_status_display')
    level = serializers.CharField(source='get_level_display')

    # creator = serializers.SerializerMethodField()
    # modifier = serializers.SerializerMethodField()
    #
    # def get_creator(self, obj):
    #     return {'account': obj.creator.account, 'username': obj.creator.username}
    #
    # def get_modifier(self, obj):
    #     return {'account': obj.modifier.account, 'username': obj.modifier.username}


if __name__ == '__main__':
    pass
