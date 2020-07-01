from django.conf.urls import url

from funds.views import OrdFundWriteViews, OrdFundReadViews, FreFundWriteViews, FreFundReadViews, CustomsFundWriteViews, \
    CustomsFundReadViews
from funds.views.other_funds_views import OthersFundWriteViews, OthersFundReadViews

urlpatterns = [
    # 订单款项模块
    url(r'^orders_fund-update/(?P<pk>\d+)$', OrdFundWriteViews.as_view({'put': 'update'})),
    url(r'^orders_fund-delete/(?P<pk>\d+)$', OrdFundWriteViews.as_view({'delete': 'destroy'})),
    url(r'^orders_fund-detail/(?P<pk>\d+)$', OrdFundReadViews.as_view({'get': 'retrieve'})),
    url(r'^orders-list$', OrdFundReadViews.as_view({'get': 'list'})),

    # 运单款项模块
    url(r'^freights-fund-update/(?P<pk>\d+)$', FreFundWriteViews.as_view({'put': 'update'})),
    url(r'^freights-fund-delete/(?P<pk>\d+)$', FreFundWriteViews.as_view({'delete': 'destroy'})),
    url(r'^freights-fund-detail/(?P<pk>\d+)$', FreFundReadViews.as_view({'get': 'retrieve'})),
    url(r'^freights-fund-list$', FreFundReadViews.as_view({'get': 'list'})),

    # 清关款项模块
    url(r'^customs-fund-update/(?P<pk>\d+)$', CustomsFundWriteViews.as_view({'put': 'update'})),
    url(r'^customs-fund-delete/(?P<pk>\d+)$', CustomsFundWriteViews.as_view({'delete': 'destroy'})),
    url(r'^customs-fund-detail/(?P<pk>\d+)$', CustomsFundReadViews.as_view({'get': 'retrieve'})),
    url(r'^customs-fund-list$', CustomsFundReadViews.as_view({'get': 'list'})),

    # 其他款项模块
    url(r'^others-fund-create/(?P<pk>\d+)$', OthersFundWriteViews.as_view({'post': 'create'})),
    url(r'^others-fund-update/(?P<pk>\d+)$', OthersFundWriteViews.as_view({'put': 'update'})),
    url(r'^others-fund-delete/(?P<pk>\d+)$', OthersFundWriteViews.as_view({'delete': 'destroy'})),
    url(r'^others-fund-detail/(?P<pk>\d+)$', OthersFundReadViews.as_view({'get': 'retrieve'})),
    url(r'^others-fund-list$', OthersFundReadViews.as_view({'get': 'list'})),
]
