from django.db import models as model0
from django_mysql import models as model1


class DataDictType(model0.Model):
    """数据字典类型模型类"""

    code = model0.CharField(max_length=32, null=True, blank=True, verbose_name='字典类型代码')
    name = model0.CharField(max_length=64, null=True, blank=True, verbose_name='字典类型名称')

    creator = model0.ForeignKey(to='UsersInfo', related_name='types_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='UsersInfo', related_name='types_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'systems'
        db_table = 's_types'
        verbose_name = '数据字典类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


if __name__ == '__main__':
    pass
