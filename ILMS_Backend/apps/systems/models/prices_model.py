from django.db import models as model0
from django_mysql import models as model1


class CusChaPri(model0.Model):
    """客户服务渠道模型"""

    owner_code = model0.CharField(max_length=32, null=True, blank=True, verbose_name='所属者代码')
    channel_code = model0.CharField(max_length=32, null=True, blank=True, verbose_name='渠道代码')
    channel_name = model0.CharField(max_length=64, null=True, blank=True, verbose_name='渠道类型')
    unit_price = model0.FloatField(max_length=12, null=True, blank=True, verbose_name='客户服务渠道单价')
    insurance_rate = model0.FloatField(max_length=12, null=True, blank=True, verbose_name='保险费率')

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='prices_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='prices_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'systems'
        db_table = 's_price'
        verbose_name = '数据字典类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner_code + self.channel.name


if __name__ == '__main__':
    pass
