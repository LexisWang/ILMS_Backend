from django.db import models as model0
from django_mysql import models as model1


class ReceiversInfo(model0.Model):
    """ 收货方模型类 """

    customer = model0.ForeignKey(to='CustomersInfo', related_name='receivers', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属者')
    code = model0.CharField(max_length=32, null=True, blank=True, verbose_name='收货方代码')
    name = model0.CharField(max_length=100, null=True, blank=True, verbose_name='收货方名称')
    company = model0.CharField(max_length=100, null=True, blank=True, verbose_name='收货方公司')
    mobile = model0.CharField(max_length=32, null=True, blank=True, verbose_name='收货方电话')
    mobile1 = model0.CharField(max_length=32, null=True, blank=True, verbose_name='收货方固定电话')
    county = model0.ForeignKey(to='systems.Countries', related_name='receivers', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='收货方国家')
    city = model0.ForeignKey(to='systems.Cities', related_name='receivers', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='收货方城市')
    postcode = model0.CharField(max_length=32, null=True, blank=True, verbose_name='收货方邮编')
    address = model0.CharField(max_length=100, null=True, blank=True, verbose_name='收货方地址')
    remark_comment = model0.TextField(max_length=300, null=True, blank=True, verbose_name='备注')

    creator = model0.ForeignKey(to='systems.UsersInfo', related_name='receivers_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='systems.UsersInfo', related_name='receivers_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'customers'
        db_table = 'i_receivers'
        verbose_name = '收货方'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


if __name__ == '__main__':
    pass
