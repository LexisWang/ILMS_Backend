from django.db import models as model0
from django_mysql import models as model1

import settings


class OrdersInfo(model0.Model):
    """订单表模型类"""

    trans_code = model0.CharField(max_length=32, null=True, blank=True, unique=True, verbose_name='转单号')
    order_status = model0.SmallIntegerField(choices=settings.ORDER_STATUS_CHOICE, default=1, verbose_name='订单状态')
    freight = model0.ForeignKey(to='FreightsInfo', related_name='orders', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属运单')
    customer = model0.ForeignKey(to='customers.CustomersInfo', related_name='orders', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属客户')
    channel = model0.ForeignKey(to='systems.DataDictsValue', related_name='orders_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属渠道')
    good_type = model0.ForeignKey(to='systems.DataDictsValue', related_name='orders_g', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属货物类型')
    pay_type = model0.ForeignKey(to='systems.DataDictsValue', related_name='orders_p', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属付款类型')
    operators = model0.ManyToManyField(to='systems.UsersInfo', related_name='users', through='Order2Operator', through_fields=('order', 'operator'), blank=True, db_index=False, verbose_name='操作员')
    collection_money = model0.FloatField(max_length=12, default=0, null=True, verbose_name='代收金额')
    v_w_rate = model0.FloatField(max_length=12, null=True, verbose_name='体积重量比')
    volume = model0.FloatField(max_length=12, null=True, verbose_name='体积')
    volume_w = model0.FloatField(max_length=12, null=True, verbose_name='体积重')
    weight = model0.FloatField(max_length=12, null=True, verbose_name='重量')
    price_w = model0.FloatField(max_length=12, null=True, verbose_name='价格重量')
    number = model0.IntegerField(null=True, verbose_name='包裹件数')
    transport_site = model1.JSONField(null=True, blank=True, verbose_name='起运地点')
    goods_name = model0.TextField(max_length=300, null=True, blank=True, verbose_name='货物名称')
    goods_name_en = model0.TextField(max_length=300, null=True, blank=True, verbose_name='货物名称(英文)')
    flight_number = model0.CharField(max_length=64, null=True, blank=True, verbose_name='航班号')
    remark_comment = model0.TextField(max_length=300, null=True, blank=True, verbose_name='备注')
    order_time = model0.DateTimeField(null=True, verbose_name="订单时间")
    receiver = model0.ForeignKey(to='customers.ReceiversInfo', related_name='orders_r', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='收货方')

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='orders_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='orders_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'business'
        db_table = 'b_orders'
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.trans_code


class Order2Operator(model0.Model):
    order = model0.ForeignKey(to='OrdersInfo', to_field='id', related_name='orders_to', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False)
    operator = model0.ForeignKey(to='systems.UsersInfo', to_field='id', related_name='operators_to', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False)

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='user_operator_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='user_operator_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'business'
        db_table = 's_order2operator'
        verbose_name = '订单/操作员-中间表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.trans_code) + str(self.operator.username)


if __name__ == '__main__':
    pass
