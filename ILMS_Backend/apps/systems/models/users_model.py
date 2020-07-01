from django.contrib.auth.models import AbstractUser
from django.db import models as model0
from django_mysql import models as model1

import settings


class UsersInfo(AbstractUser):
    """用户模型类"""

    account = model1.SetCharField(base_field=model0.CharField(max_length=16), size=4, max_length=67, null=True, blank=True, verbose_name='账号')
    mobile = model1.SetCharField(base_field=model0.CharField(max_length=16), size=4, max_length=67, null=True, blank=True, verbose_name='手机号')
    status = model0.SmallIntegerField(choices=settings.STATUS_USE_CHOICE, default=1, null=True, blank=True, verbose_name='是否启用')
    bran = model0.ForeignKey(to='BranchesInfo', to_field='id', related_name='users', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='所属分部')
    roles = model0.ManyToManyField(to='RolesInfo', related_name='users', through='UsersRoles', through_fields=('user', 'role'), blank=True, db_index=False, verbose_name='所属角色')

    creator = model0.ForeignKey(to='self', related_name='users_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='self', related_name='users_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'systems'
        db_table = 's_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


if __name__ == '__main__':
    pass
