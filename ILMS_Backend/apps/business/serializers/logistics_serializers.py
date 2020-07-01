from datetime import datetime

import pytz
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from ..models import LogisticsInfo, LogisticTemplate


# 物流信息反序列化器
class LogisticsSerAnti(serializers.ModelSerializer):
    """物流信息系反列化器"""

    class Meta:
        model = LogisticsInfo
        fields = [
            'id',
            'order',
            'freight',
            'process_zh',
            'process_en',
            'time_dot',
        ]
        extra_kwargs = {
            'id': {'help_text': 'ID', 'read_only': True},
        }

    def create(self, validated_data):
        request_user = self.context.get('request').user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['creator'] = request_user
        validated_data['modifier'] = validated_data.get('creator')

        time_dot = validated_data.get('time_dot')
        if not time_dot:
            now_time = datetime.today()
            datetime(year=now_time.year, month=now_time.month, day=now_time.day, hour=now_time.hour,
                     minute=now_time.minute, second=now_time.second,
                     tzinfo=pytz.timezone('Asia/Shanghai'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request_user = self.context.get('request').user
        if isinstance(request_user, AnonymousUser):
            request_user = None
        validated_data['modifier'] = request_user
        return super().update(instance, validated_data)


# 物流信息序列化器
class LogisticsSer(LogisticsSerAnti):
    """物流信息系反列化器"""

    order = serializers.StringRelatedField()
    freight = serializers.StringRelatedField()
    time_dot = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')


# 物流模板序列化器
class LogisticTemplateSer(serializers.ModelSerializer):
    """物流模板序列化器"""

    class Meta:
        model = LogisticTemplate
        fields = '__all__'


if __name__ == '__main__':
    pass

