# import os
# import sys
#
# if not os.getenv('DJANGO_SETTINGS_MODULE'):
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'ILMS_Backend.settings'
#
# import django
#
# django.setup()
#
# import settings
#
# from systems.models import Countries, Cities
# from django.db.models import Q, F
# from rest_framework import serializers
# from business.models import OrdersInfo

if __name__ == '__main__':
    # 查询字段重命名
    # data = Countries.objects.prefetch_related('cities').values('code', 名称=F('name'))

    # data = OrdersInfo.objects.values('customer__salesman__username')

    name = 'lexis'
    print(name)
    print('123')
