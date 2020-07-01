from django.db import models as model0
from django_mysql import models as model1

import settings


class BranchesInfo(model0.Model):
    """分部信息模型"""

    name = model0.CharField(max_length=64, null=True, blank=True, verbose_name="分部名称")
    desc = model0.TextField(max_length=300, null=True, blank=True, verbose_name="分部描述")
    status = model0.SmallIntegerField(choices=settings.STATUS_USE_CHOICE, default=1, null=True, blank=True, verbose_name='是否启用')

    creator = model0.ForeignKey(to='UsersInfo', related_name='branches_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='UsersInfo', related_name='branches_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'systems'
        db_table = 's_branch'
        verbose_name = '分部'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


if __name__ == '__main__':
    pass
