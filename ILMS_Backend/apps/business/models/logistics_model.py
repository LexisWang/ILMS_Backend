from django.db import models as model0
from django_mysql import models as model1


class LogisticsInfo(model0.Model):
    """物流信息模型了"""

    order = model0.ForeignKey(to='OrdersInfo', related_name='logistics', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属订单')
    freight = model0.ForeignKey(to='FreightsInfo', related_name='logistics', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属运单')
    process_zh = model0.CharField(max_length=300, null=True, blank=True, verbose_name='进度(中文)')
    process_en = model0.CharField(max_length=300, null=True, blank=True, verbose_name='进度(英文)')
    time_dot = model0.DateTimeField(verbose_name='时间点')

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='logistics_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='logistics_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'business'
        db_table = 'b_logistics'
        verbose_name = '物流信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class LogisticTemplate(model0.Model):
    """物流模板"""

    process_zh = model0.CharField(max_length=300, verbose_name='进度(中文)')
    process_en = model0.CharField(max_length=300, verbose_name='进度(英文)')

    class Meta:
        app_label = 'business'
        db_table = 'b_logistic_template'
        verbose_name = '物流模板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


if __name__ == '__main__':
    pass
