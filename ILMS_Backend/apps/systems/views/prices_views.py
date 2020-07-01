from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

import settings
from utils.list_pages import CusResponse, ReadModelViewSetPlus, WriteModelViewSetPlus
from ..models import CusChaPri, DataDictType
from ..serializers import ChaPriSerializer
from ..utils import PricesFilterSet


# 价格读视图集
class PricesReadViews(ReadModelViewSetPlus):
    """价格读视图集"""

    queryset = CusChaPri.objects.all()
    serializer_class = ChaPriSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PricesFilterSet
    pagination_class = CusResponse

    def list(self, request, *args, **kwargs):
        owner_code = self.request.query_params.get('owner_code')
        type_id = DataDictType.objects.get(code=settings.CHAN_CODE).id
        queryset = CusChaPri.objects.raw(
            raw_query="""
                select a.id, %s owner_code, a.code channel_code, a.name channel_name, b.unit_price, b.insurance_rate,
                b.creator_id, b.modifier_id, b.create_time, b.modify_time
                    from s_values a
                left join s_price b on a.code = b.channel_code
                where a.type_id = %s
                  and a.status = 1
                order by a.create_time desc
            """,
            params=[owner_code, type_id]
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 价格写视图集
class PricesWriteViews(WriteModelViewSetPlus):
    """价格写视图集"""

    queryset = CusChaPri.objects.all()
    serializer_class = ChaPriSerializer

    def update(self, request, *args, **kwargs):
        owner_code = self.request.data.get('owner_code')
        channel_code = self.request.data.get('channel_code')
        instance = CusChaPri.objects.filter(Q(owner_code=owner_code) & Q(channel_code=channel_code))
        if len(instance) < 1:
            if not self.request.data.get('unit_price'):
                return CusResponse.get_response(success=False, message='该渠道价格不能为空', code=settings.FALSE_CODE)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return CusResponse.get_response(serializer.data)
        else:
            if not self.request.data.get('unit_price'):
                instance.delete()
                return CusResponse.get_response(success=True)
            else:
                serializer = self.get_serializer(instance[0], data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                if getattr(instance, '_prefetched_objects_cache', None):
                    instance._prefetched_objects_cache = {}
                return CusResponse.get_response(serializer.data)


if __name__ == '__main__':
    pass
