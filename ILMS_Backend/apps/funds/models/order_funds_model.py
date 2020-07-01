from django.db import models as model0
from django_mysql import models as model1

import settings


class OrdFundsInfo(model0.Model):
    """订单款项 模型类"""

    order = model0.ForeignKey(to='business.OrdersInfo', related_name='order_funds', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属订单')
    customer = model0.ForeignKey(to='customers.CustomersInfo', related_name='order_funds', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属客户')
    fund_status = model0.SmallIntegerField(choices=settings.FUND_STATUS_CHOICE, default=1, verbose_name='款项状态')
    order_status = model0.SmallIntegerField(choices=settings.ORDER_STATUS_CHOICE, default=1, verbose_name='订单状态')
    pay_type = model0.ForeignKey(to='systems.DataDictsValue', related_name='order_funds_p', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属付款类型')
    channel = model0.ForeignKey(to='systems.DataDictsValue', related_name='order_funds_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属渠道')
    service = model0.ForeignKey(to='systems.UsersInfo', related_name='order_funds_s', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='款项专员')
    price_w = model0.FloatField(max_length=12, null=True, verbose_name='价格重量')
    insurance_rate = model0.FloatField(max_length=12, null=True, verbose_name='保险费率', default=0)
    y_account = model0.FloatField(max_length=12, null=True, verbose_name='应收金额')
    s_account = model0.FloatField(max_length=12, null=True, verbose_name='实收金额', default=0)
    j_account = model0.FloatField(max_length=12, null=True, verbose_name='减免金额', default=0)
    w_account = model0.FloatField(max_length=12, null=True, verbose_name='未结算金额')
    freight_fee = model0.FloatField(max_length=12, null=True, verbose_name='运费')
    dispatch_fee = model0.FloatField(max_length=12, null=True, verbose_name='派送费', default=0)
    file_fee = model0.FloatField(max_length=12, null=True, verbose_name='文件费', default=0)
    operate_fee = model0.FloatField(max_length=12, null=True, verbose_name='操作费', default=0)
    insurance_fee = model0.FloatField(max_length=12, null=True, verbose_name='保险费', default=0)
    server_fee = model0.FloatField(max_length=12, null=True, verbose_name='服务费', default=0)
    insurance_money = model0.FloatField(max_length=12, null=True, verbose_name='保险金额', default=0)
    collection_money = model0.FloatField(max_length=12, null=True, verbose_name='代收金额')
    other_fee = model0.FloatField(max_length=12, null=True, verbose_name='其他费用', default=0)
    remark_comment = model0.TextField(max_length=300, null=True, blank=True, verbose_name='减免说明')
    attachment_ids = model1.JSONField(null=True, blank=True, verbose_name='附件列表')
    order_time = model0.DateTimeField(null=True, verbose_name="订单时间")

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='order_funds_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='order_funds_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'funds'
        db_table = 'b_ord_funds'
        verbose_name = '订单款项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.trans_code


if __name__ == '__main__':
    pass
