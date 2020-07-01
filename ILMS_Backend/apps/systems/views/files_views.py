import logging
import os

from utils.list_pages import CusResponse, ReadModelViewSetPlus
from ..models import FileInfo
from ..serializers import FilesSerializers


# 文件读视图集
class FilesWriteViews(ReadModelViewSetPlus):
    """文件视图集"""

    queryset = FileInfo.objects.all()
    serializer_class = FilesSerializers
    pagination_class = CusResponse

    def get_queryset(self):
        return self._get_queryset(user=self.request.user, queryset=self.queryset, model=FileInfo)

    def create(self, request, *args, **kwargs):
        # 创建日志记录器
        logger = logging.getLogger('django')
        data = []
        for i in range(len(request.data.getlist('file_name'))):
            datum = {
                'name': self.request.data.getlist('file_name')[i],
                'format': self.request.data.getlist('file_content_type')[i],
                'file_path': self.request.data.getlist('file_path')[i] + '.' + self.request.data.getlist('file_content_type')[i].split('/')[-1],
                'md5_value': self.request.data.getlist('file_md5')[i],
                'size': self.request.data.getlist('file_size')[i],
            }
            data.append(datum)
            os.rename(self.request.data.getlist('file_path')[i], self.request.data.getlist('file_path')[i] + '.' + self.request.data.getlist('file_content_type')[i].split('/')[-1])
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CusResponse.get_response(data=serializer.data, message='文件上传成功！')


if __name__ == '__main__':
    pass
