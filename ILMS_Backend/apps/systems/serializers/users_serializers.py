from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from rest_framework import serializers

from ..models import UsersInfo, RolesInfo, BranchesInfo


# 用户更新序列化器
class UserUpdateSerializer(serializers.Serializer):
    account = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False)
    bran = serializers.PrimaryKeyRelatedField(label='所属分部', help_text='所属分部', queryset=BranchesInfo.objects.all(), required=False)
    roles = serializers.ManyRelatedField(
        child_relation=serializers.PrimaryKeyRelatedField(label='所属角色', help_text='用户关联的角色',
                                                          queryset=RolesInfo.objects.all()), help_text='用户关联的角色',
        required=False, label='所属角色')

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles')
        request_user = self.context.get('request').user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['modifier'] = request_user

        with transaction.atomic():
            for attr in validated_data.keys():
                setattr(instance, attr, validated_data.get(attr))
            instance.roles.set(roles)
            instance.save()
        return instance


# 用户创建序列化器
class UsersSerializerAnti(serializers.ModelSerializer):
    """用户序列反化器"""

    roles = serializers.ManyRelatedField(
        child_relation=serializers.PrimaryKeyRelatedField(label='所属角色', help_text='用户关联的角色',
                                                          queryset=RolesInfo.objects.all()), help_text='用户关联的角色',
        required=False, label='所属角色')
    creator = serializers.StringRelatedField(read_only=True)
    modifier = serializers.SlugRelatedField(read_only=True, slug_field='username')
    date_joined = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UsersInfo
        fields = [
            'id',
            'account',
            'username',
            'password',
            'mobile',
            'status',
            'bran',
            'roles',
            'creator',
            'modifier',
            'date_joined',
            'modify_time',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        roles = validated_data.pop('roles')
        request_user = self.context.get('request').user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['creator'] = request_user
        validated_data['modifier'] = validated_data.get('creator')

        with transaction.atomic():
            user = UsersInfo.objects.create_user(**validated_data)
            user.roles.set(roles)
            user.save()
        return user


# 用户读取序列化器
class UsersSerializer(UsersSerializerAnti):
    """角色序列化器"""

    status = serializers.CharField(source='get_status_display')
    bran = serializers.StringRelatedField()
    roles = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    date_joined = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    # creator = serializers.SerializerMethodField()
    # modifier = serializers.SerializerMethodField()
    #
    # def get_creator(self, obj):
    #     return {'account': obj.creator.account, 'username': obj.creator.username}
    #
    # def get_modifier(self, obj):
    #     return {'account': obj.modifier.account, 'username': obj.modifier.username}


# 用户登陆
class JwtLogSerializer(serializers.Serializer):
    """JWT登录序列化器"""

    account = serializers.CharField(max_length=64, write_only=True, help_text='用户名称 长度小于64')
    password = serializers.CharField(max_length=64, write_only=True, help_text='用户账号 长度小于64')


# 修改密码
class UpdatePasswordSerial(serializers.Serializer):
    old_password = serializers.CharField(help_text='旧密码')
    new_password = serializers.CharField(help_text='新密码')
    ensure_password = serializers.CharField(help_text='确认密码')


if __name__ == '__main__':
    pass
