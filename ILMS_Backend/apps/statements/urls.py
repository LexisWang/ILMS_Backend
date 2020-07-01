from django.conf.urls import url

from .views import OrderReportQueryViews, OrderPandasViews, FreightReportQueryViews, FreightPandasViews

urlpatterns = [
    # 订单报表
    url(r'^orders-statement-query$', OrderReportQueryViews.as_view()),
    url(r'^orders-statement-export$', OrderPandasViews.as_view()),

    # 运单报表
    url(r'^freights-statement-query$', FreightReportQueryViews.as_view()),
    url(r'^freights-statement-export$', FreightPandasViews.as_view()),
]
