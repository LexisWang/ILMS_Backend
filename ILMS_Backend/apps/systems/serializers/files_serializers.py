from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import FileInfo


class FilesSerializers(serializers.ModelSerializer):
    """文件序列化器"""

    file_path = serializers.CharField(write_only=True, required=True, help_text='文件路径')
    creator = serializers.StringRelatedField(read_only=True)
    modifier = serializers.SlugRelatedField(read_only=True, slug_field='username')
    create_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    modify_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = FileInfo
        fields = [
            'id',
            'owner',
            'name',
            'format',
            'file_path',
            'creator',
            'modifier',
            'create_time',
            'modify_time',
            'md5_value',
            'size',
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


if __name__ == '__main__':
    pass
