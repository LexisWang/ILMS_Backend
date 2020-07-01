from django.db import models as model0
from django_mysql import models as model1

import settings


class CustomsFundsInfo(model0.Model):
    """清关款项 模型类"""

    type = model0.SmallIntegerField(choices=settings.CUSTOMS_LEVEL_CHOICE, default=1, verbose_name='类型')
    freight = model0.ForeignKey(to='business.FreightsInfo', related_name='custom_funds', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属运单')
    fund_status = model0.SmallIntegerField(choices=settings.FUND_STATUS_CHOICE, default=1, verbose_name='款项状态')
    channel = model0.ForeignKey(to='systems.DataDictsValue', related_name='custom_funds_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属渠道')
    service = model0.ForeignKey(to='systems.UsersInfo', related_name='custom_funds_s', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='款项专员')
    y_account = model0.FloatField(max_length=12, null=True, verbose_name='应付金额')
    s_account = model0.FloatField(max_length=12, null=True, verbose_name='实付金额', default=0)
    j_account = model0.FloatField(max_length=12, null=True, verbose_name='减免金额', default=0)
    w_account = model0.FloatField(max_length=12, null=True, verbose_name='未结算金额')
    customs_fee = model0.FloatField(max_length=12, null=True, verbose_name='清关费', default=0)
    remark_comment = model0.TextField(max_length=300, null=True, blank=True, verbose_name='减免说明')
    attachment_ids = model1.JSONField(null=True, blank=True, verbose_name='附件列表')
    pack_time = model0.DateTimeField(null=True, blank=True, verbose_name="打包时间")

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='custom_funds_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='custom_funds_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'funds'
        db_table = 'b_customs_funds'
        verbose_name = '货运款项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.freight.freight_code


if __name__ == '__main__':
    pass
