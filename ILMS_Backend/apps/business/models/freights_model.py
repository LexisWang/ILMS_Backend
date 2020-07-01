from django.db import models as model0
from django_mysql import models as model1

import settings


class FreightsInfo(model0.Model):
    """运单 模型类"""

    freight_code = model0.CharField(max_length=32, null=True, blank=True, verbose_name='运单号')
    freight_status = model0.SmallIntegerField(choices=settings.FREIGHT_STATUS_CHOICE, default=1, verbose_name='运单状态')
    channel = model0.ForeignKey(to='systems.DataDictsValue', related_name='freights_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属渠道')
    pay_type = model0.ForeignKey(to='systems.DataDictsValue', related_name='freights_p', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属付款类型')
    trans_company = model0.ForeignKey(to='systems.DataDictsValue', related_name='freights_t', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='货运公司')
    mid_company = model0.ForeignKey(to='systems.DataDictsValue', related_name='freights_m', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='中港公司')
    kits = model0.IntegerField(null=True, verbose_name='货物件数')
    weight = model0.FloatField(max_length=12, null=True, verbose_name='总重量')
    volume = model0.FloatField(max_length=12, null=True, verbose_name='总体积')
    price_w = model0.FloatField(max_length=12, null=True, verbose_name='价格重')
    volume_w = model0.FloatField(max_length=12, null=True, verbose_name='体积重')
    collection_money = model0.FloatField(max_length=12, null=True, verbose_name='代收金额')
    transport_site = model1.JSONField(null=True, blank=True, verbose_name='起运地点')
    order_codes = model1.JSONField(max_length=1000, null=True, blank=True, verbose_name='订单号')
    mid_port = model0.CharField(max_length=100, null=True, blank=True, verbose_name='中转站')
    flight_number = model0.CharField(max_length=64, null=True, blank=True, verbose_name='航班号')
    remark_comment = model0.TextField(max_length=300, null=True, blank=True, verbose_name='备注')
    pack_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="打包时间")

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='freights_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='freights_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'business'
        db_table = 'b_freights'
        verbose_name = '运单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.freight_code


if __name__ == '__main__':
    pass
