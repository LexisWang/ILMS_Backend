from django.db import models as model0
from django_mysql import models as model1

import settings


class FreFundsInfo(model0.Model):
    """货运款项 模型类"""

    freight = model0.ForeignKey(to='business.FreightsInfo', related_name='freight_funds', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属运单')
    fund_status = model0.SmallIntegerField(choices=settings.FUND_STATUS_CHOICE, default=1, verbose_name='款项状态')
    freight_status = model0.SmallIntegerField(choices=settings.FREIGHT_STATUS_CHOICE, default=1, verbose_name='运单状态')
    pay_type = model0.ForeignKey(to='systems.DataDictsValue', related_name='freight_funds_p', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属付款类型')
    trans_company = model0.ForeignKey(to='systems.DataDictsValue', related_name='freight_funds_t', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='货运公司')
    mid_company = model0.ForeignKey(to='systems.DataDictsValue', related_name='freights_funds_m', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='中港公司')
    channel = model0.ForeignKey(to='systems.DataDictsValue', related_name='freight_funds_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属渠道')
    service = model0.ForeignKey(to='systems.UsersInfo', related_name='freight_funds_s', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='款项专员')
    price_w = model0.FloatField(max_length=12, null=True, verbose_name='价格重量')
    y_account = model0.FloatField(max_length=12, null=True, verbose_name='应付金额')
    s_account = model0.FloatField(max_length=12, null=True, verbose_name='实付金额', default=0)
    j_account = model0.FloatField(max_length=12, null=True, verbose_name='减免金额', default=0)
    w_account = model0.FloatField(max_length=12, null=True, verbose_name='未结算金额')
    freight_fee = model0.FloatField(max_length=12, null=True, verbose_name='运费')
    lading_fee = model0.FloatField(max_length=12, null=True, verbose_name='提单费', default=0)
    magntest_fee = model0.FloatField(max_length=12, null=True, verbose_name='磁检费', default=0)
    operate_fee = model0.FloatField(max_length=12, null=True, verbose_name='操作费', default=0)
    file_fee = model0.FloatField(max_length=12, null=True, verbose_name='文件费', default=0)
    custclea_fee = model0.FloatField(max_length=12, null=True, verbose_name='报关费', default=0)
    collection_money = model0.FloatField(max_length=12, null=True, verbose_name='代付金额')
    other_fee = model0.FloatField(max_length=12, null=True, verbose_name='其他费用', default=0)
    remark_comment = model0.TextField(max_length=300, null=True, blank=True, verbose_name='减免说明')
    attachment_ids = model1.JSONField(null=True, blank=True, verbose_name='附件列表')
    pack_time = model0.DateTimeField(null=True, verbose_name="打包时间")

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='freight_funds_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='freight_funds_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'funds'
        db_table = 'b_fre_funds'
        verbose_name = '货运款项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.freight.freight_code


if __name__ == '__main__':
    pass
