from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

import settings
from utils.list_pages import MySearchFilter, CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import LogisticsInfo, LogisticTemplate, OrdersInfo
from ..serializers import LogisticsSerAnti, LogisticsSer, LogisticTemplateSer
from ..utils import LogisticFilterSet


# 物流信息读视图集
class LogisticsReadViews(ReadModelViewSetPlus):
    """物流信息读视图集"""

    queryset = LogisticsInfo.objects.all()
    serializer_class = LogisticsSer
    filter_backends = [DjangoFilterBackend, MySearchFilter]
    filterset_class = LogisticFilterSet
    pagination_class = CusResponse
    search_fields = ['process_zh', 'process_en']


# 物流信息写视图集
class LogisticsWriteViews(WriteModelViewSetPlus):
    """物流信息写视图集"""

    queryset = LogisticsInfo.objects.all()
    serializer_class = LogisticsSerAnti
    filter_backends = [DjangoFilterBackend, MySearchFilter]

    def create(self, request, *args, **kwargs):
        if not self.request.data.get('order') or not self.request.data.get('freight'):
            return CusResponse.get_response(success=False, message='缺少订单或运单', code=settings.FALSE_CODE)
        if not self.request.data.get('process_zh'):
            return CusResponse.get_response(success=False, message='缺少物流信息描述', code=settings.FALSE_CODE)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        order = self.request.query_params.get('order')
        freight = self.request.query_params.get('freight')
        if order and order.isdigit():
            order = int(order)
            order = OrdersInfo.objects.get(id=order)
            instance1 = LogisticsInfo.objects.filter(order=order)
            instance2 = LogisticsInfo.objects.filter(freight=order.freight)
            return instance1.union(instance2)
        elif freight and freight.isdigit():
            freight = int(freight)
            return LogisticsInfo.objects.filter(freight=freight)
        else:
            return LogisticsInfo.objects.none()


class LogisticTemplateView(ModelViewSet):
    """物流信息模板视图集"""

    queryset = LogisticTemplate.objects.all()
    serializer_class = LogisticTemplateSer


if __name__ == '__main__':
    pass
