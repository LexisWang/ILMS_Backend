from django.views.static import serve
from rest_framework.decorators import api_view


@api_view(http_method_names=['get'])
def custom_static_server(request, path, document_root=None, show_indexes=False):
    """自定义的响应静态文件"""
    return serve(request, path, document_root=document_root, show_indexes=show_indexes)
