from django.db import models as model0
from django_mysql import models as model1

import settings


class RolesInfo(model0.Model):
    """角色：绑定权限"""

    name = model0.CharField(max_length=64, null=True, blank=True, verbose_name='角色名称')
    desc = model0.TextField(max_length=300, null=True, blank=True, verbose_name='角色描述')
    status = model0.SmallIntegerField(choices=settings.STATUS_USE_CHOICE, default=1, null=True, verbose_name='是否启用')
    level = model0.SmallIntegerField(choices=settings.DATA_LEVEL_CHOICE, default=3, null=True, verbose_name='数据级别')
    menu_list = model1.JSONField(null=True, blank=True, verbose_name='菜单权限')

    creator = model0.ForeignKey(to='UsersInfo', related_name='roles_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='UsersInfo', related_name='roles_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'systems'
        db_table = 's_roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


if __name__ == '__main__':
    pass
