from django.conf.urls import url

from .views import CustomersWriteViews, CustomersReadViews, CheckCusCode, ReceiversWriteViews, ReceiversReadViews, \
    CheckRecCode, GetCusOptionsView, RecOptionsView, CityOptionsView

urlpatterns = [
    # 客户方模块
    url(r'^customers-create$', CustomersWriteViews.as_view({'post': 'create'})),
    url(r'^customers-update/(?P<pk>\d+)$', CustomersWriteViews.as_view({'put': 'update'})),
    url(r'^customers-delete/(?P<pk>\d+)$', CustomersWriteViews.as_view({'delete': 'destroy'})),
    url(r'^customers-detail/(?P<pk>\d+)$', CustomersReadViews.as_view({'get': 'retrieve'})),
    url(r'^customers-list$', CustomersReadViews.as_view({'get': 'list'})),
    url(r'^customers-check$', CheckCusCode.as_view()),

    # 收货方模块
    url(r'^receivers-create$', ReceiversWriteViews.as_view({'post': 'create'})),
    url(r'^receivers-update/(?P<pk>\d+)$', ReceiversWriteViews.as_view({'put': 'update'})),
    url(r'^receivers-delete/(?P<pk>\d+)$', ReceiversWriteViews.as_view({'delete': 'destroy'})),
    url(r'^receivers-detail/(?P<pk>\d+)$', ReceiversReadViews.as_view({'get': 'retrieve'})),
    url(r'^receivers-list$', ReceiversReadViews.as_view({'get': 'list'})),
    url(r'^receivers-check$', CheckRecCode.as_view()),

    # 创建客户方的前提
    url(r'^custmer-options$', GetCusOptionsView.as_view()),

    # 创建收货方的前提
    url(r'^receiver-options$', RecOptionsView.as_view()),

    # 创建收货方的前提(城市)
    url(r'^receiver-cities$', CityOptionsView.as_view()),
]
