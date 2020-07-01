from django.db import models as model0
from django_mysql import models as model1

import settings


class OtherFundsInfo(model0.Model):
    """其他款项"""
    fund_code = model0.CharField(max_length=32, null=True, blank=True, verbose_name='款号')
    fund_type = model0.SmallIntegerField(choices=settings.OTHER_FUND_TYPE_CHOICE, null=True, verbose_name='款项类型')
    fund_status = model0.SmallIntegerField(choices=settings.FUND_STATUS_CHOICE, default=1, verbose_name='款项状态')
    order = model0.ForeignKey(to='business.OrdersInfo', related_name='other_funds_o', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属订单')
    freight = model0.ForeignKey(to='business.FreightsInfo', related_name='other_funds_f', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属运单')
    service = model0.ForeignKey(to='systems.UsersInfo', related_name='other_funds_s', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='款项专员')
    payee_payer = model0.CharField(max_length=64, null=True, blank=True, verbose_name='收/付款方名称')
    connect_ways = model0.CharField(max_length=32, null=True, blank=True, verbose_name='收/付款方联系方式')
    y_account = model0.FloatField(max_length=12, null=True, verbose_name='应收/付金额')
    s_account = model0.FloatField(max_length=12, null=True, verbose_name='实收/付金额')
    remark_comment = model0.TextField(max_length=300, null=True, blank=True, verbose_name='款项说明')
    attachment_ids = model1.JSONField(null=True, blank=True, verbose_name='附件列表')
    recpay_time = model0.DateField(null=True, verbose_name="收/付款时间")

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='other_funds_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='other_funds_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'funds'
        db_table = 'b_oth_funds'
        verbose_name = '其他款项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fund_code


if __name__ == '__main__':
    pass
