from django.db import models as model0
from django_mysql import models as model1


class CustomersInfo(model0.Model):
    """ 客户模型类 """

    code = model0.CharField(max_length=32, null=True, verbose_name='客户代码')
    name = model0.CharField(max_length=100, null=True, verbose_name='客户名称')
    rank = model0.ForeignKey(to='systems.DataDictsValue', related_name='customers', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='客户级别')
    salesman = model0.ForeignKey(to='systems.UsersInfo', related_name='customers_b', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='业务员')
    service = model0.ForeignKey(to='systems.UsersInfo', related_name='customers_s', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='客服专员')
    president_name = model0.CharField(max_length=64, null=True, verbose_name='客户方负责人')
    connect_ways = model0.CharField(max_length=32, null=True, verbose_name='联系方式')
    customer_address = model0.CharField(max_length=100, null=True, verbose_name='客户地址')
    manage_directions = model0.TextField(max_length=300, null=True, verbose_name='客户经营方向')
    remark_comment = model0.TextField(max_length=300, null=True, verbose_name='备注')
    attachment_ids = model1.JSONField(null=True, blank=True, verbose_name='附件列表')

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='customers_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='customers_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'customers'
        db_table = 'i_customers'
        verbose_name = '客户方'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


if __name__ == '__main__':
    pass
