from django.db import models as model0
from django_mysql import models as model1


class FileInfo(model0.Model):
    """文件信息模型类"""

    owner = model0.CharField(max_length=64, null=True, blank=True,  verbose_name='所属者')
    name = model0.CharField(max_length=64, null=True, blank=True,  verbose_name='文件名')
    format = model0.CharField(max_length=32, null=True, blank=True,  verbose_name='文件格式')
    file_path = model0.FileField(null=True, blank=True, verbose_name='文件路径', upload_to='static/files')

    creator = model0.ForeignKey(to='UsersInfo', related_name='files_c', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='创建人')
    modifier = model0.ForeignKey(to='UsersInfo', related_name='files_u', on_delete=model0.SET_NULL, null=True, blank=True, db_constraint=False, db_index=False, verbose_name='修改人')
    create_time = model0.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    modify_time = model0.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")
    md5_value = model0.CharField(max_length=32, null=True, blank=True, verbose_name='文件格式')
    size = model0.CharField(max_length=32, null=True, blank=True, verbose_name='文件大小')

    class Meta:
        app_label = 'systems'
        db_table = 'b_files'
        verbose_name = '文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


if __name__ == '__main__':
    pass
