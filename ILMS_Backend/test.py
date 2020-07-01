import os
import sys

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ILMS_Backend.settings'

import django

django.setup()

import settings

from systems.models import Countries, Cities, DataDictsValue
from systems.serializers import DictValuesSerializer
from django.db.models import Q, F
from rest_framework import serializers
from business.models import OrdersInfo
import pandas as pd

ini = 0

def reset_index(value):
    global ini
    if value == '小计' or value == '合计':
        ini = 0
        return value
    else:
        ini += 1
        return ini

if __name__ == '__main__':
    # 查询字段重命名
    # data = Countries.objects.prefetch_related('cities').values('code', 名称=F('name'))

    # data = OrdersInfo.objects.values('customer__salesman__username')

    df = pd.DataFrame({
        'name': ['zs', 'ls', 'ls', 'ww'],
        'age': [12, 23, 34, 34],
        'height': [165, 165, 175, 185]
    })
    print(df)
    sub_total = df[['name', 'age', 'height']].groupby('name').sum()
    sub_total['name'] = ['name' for i in range(len(sub_total.index))]
    # print(df[['name', 'age', 'height']].groupby('name').sum().T)
    print(sub_total)
