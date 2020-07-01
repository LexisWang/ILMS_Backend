"""ILMS_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include

from rest_framework.documentation import include_docs_urls

from .views import custom_static_server

urlpatterns = [
    url(r'', include_docs_urls(title='ILMS_Backend API')),
    url('admin/', admin.site.urls),
    url('^api/ilms-back/systmes-mgr/', include('systems.urls')),
    url('^api/ilms-back/customers-mgr/', include('customers.urls')),
    url('^api/ilms-back/business-mgr/', include('business.urls')),
    url('^api/ilms-back/statemants-mgr/', include('statements.urls')),

    # 静态文件访问路径
    # url(r'^media/(?P<path>.*)$', custom_static_server, {'document_root': settings.MEDIA_ROOT}, name='media')
]
