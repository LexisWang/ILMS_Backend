from django.conf.urls import url

from .views import OrderWriteViews, OrderReadViews, CustomersListView, OrderOptionView, FreightWriteViews, \
    FreightReadViews, FreightOptionView, LogisticsWriteViews, LogisticsReadViews

urlpatterns = [
    # 订单模块
    url(r'^orders-create$', OrderWriteViews.as_view({'post': 'create'})),
    url(r'^orders-update/(?P<pk>\d+)$', OrderWriteViews.as_view({'put': 'update'})),
    url(r'^orders-delete/(?P<pk>\d+)$', OrderWriteViews.as_view({'delete': 'destroy'})),
    url(r'^orders-detail/(?P<pk>\d+)$', OrderReadViews.as_view({'get': 'retrieve'})),
    url(r'^orders-list$', OrderReadViews.as_view({'get': 'list'})),

    url(r'^orders-customers$', CustomersListView.as_view()),
    url(r'^orders-options$', OrderOptionView.as_view()),

    # 运单模块
    url(r'^freights-create$', FreightWriteViews.as_view({'post': 'create'})),
    url(r'^freights-update/(?P<pk>\d+)$', FreightWriteViews.as_view({'put': 'update'})),
    url(r'^freights-delete/(?P<pk>\d+)$', FreightWriteViews.as_view({'delete': 'destroy'})),
    url(r'^freights-detail/(?P<pk>\d+)$', FreightReadViews.as_view({'get': 'retrieve'})),
    url(r'^freights-list$', FreightReadViews.as_view({'get': 'list'})),

    url(r'^freights-options1$', FreightOptionView.as_view()),
    url(r'^freights-options2$', FreightOptionView.as_view()),

    # 物流信息模块
    url(r'^logistics-create$', LogisticsWriteViews.as_view({'post': 'create'})),
    url(r'^logistics-update/(?P<pk>\d+)$', LogisticsWriteViews.as_view({'put': 'update'})),
    url(r'^logistics-delete/(?P<pk>\d+)$', LogisticsWriteViews.as_view({'delete': 'destroy'})),
    url(r'^logistics-list$', LogisticsReadViews.as_view({'get': 'list'})),

    # 物流信息模板
    url(r'^template-create$', LogisticsWriteViews.as_view({'post': 'create'})),
    url(r'^template-update/(?P<pk>\d+)$', LogisticsWriteViews.as_view({'put': 'update'})),
    url(r'^template-delete/(?P<pk>\d+)$', LogisticsWriteViews.as_view({'delete': 'destroy'})),
    url(r'^template-list$', LogisticsReadViews.as_view({'get': 'list'})),
]
