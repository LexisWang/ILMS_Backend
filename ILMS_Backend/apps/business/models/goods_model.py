from django.db import models as model0
from django_mysql import models as model1

import settings


class GoodsInfo(model0.Model):
    """货物详情"""

    type = model0.SmallIntegerField(choices=settings.GOOD_VIRTUAL_CHOICE, default=1, null=True, blank=True, verbose_name='是否真实数据')
    order = model0.ForeignKey(to='OrdersInfo', related_name='goods', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属订单')
    name = model0.CharField(max_length=100, null=True, blank=True, verbose_name='货物名称')
    weight = model0.FloatField(max_length=12, null=True, verbose_name='重量')
    kits = model0.IntegerField(null=True, verbose_name='货物件数')
    number = model0.IntegerField(null=True, verbose_name='货物数量')
    length = model0.FloatField(max_length=12, null=True, verbose_name='货物长')
    width = model0.FloatField(max_length=12, null=True, verbose_name='货物宽')
    height = model0.FloatField(max_length=12, null=True, verbose_name='货物高')
    volume = model0.FloatField(max_length=12, null=True, verbose_name='货物体积')
    declared_price = model0.FloatField(max_length=12, null=True, verbose_name='申报价格')
    sku_name = model0.CharField(max_length=64, null=True, blank=True, verbose_name='SKU名称')
    customs_code = model0.CharField(max_length=32, null=True, blank=True, verbose_name='海关编码')

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='goods_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='goods_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'business'
        db_table = 'b_goods'
        verbose_name = '货物'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


if __name__ == '__main__':
    pass
