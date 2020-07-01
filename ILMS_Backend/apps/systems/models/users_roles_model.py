from django.db import models as model0
from django_mysql import models as model1


class UsersRoles(model0.Model):
    user = model0.ForeignKey(to='UsersInfo', to_field='id', related_name='user_to', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False)
    role = model0.ForeignKey(to='RolesInfo', to_field='id', related_name='role_to', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False)

    creator = model0.ForeignKey(to='UsersInfo', related_name='user_role_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='UsersInfo', related_name='user_role_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")

    class Meta:
        app_label = 'systems'
        db_table = 's_user2role'
        verbose_name = '用户/角色-中间表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user.username) + str(self.role.name)


if __name__ == '__main__':
    pass
