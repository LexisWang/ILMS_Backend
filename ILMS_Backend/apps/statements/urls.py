from django.conf.urls import url

from .views import OrderReportQueryViews, OrderExportSingleViews, OrderExportPluralViews, \
    OrderReportStatisticsSingleViews, OrderReportStatisticsPluralViews, FreightReportQueryViews, \
    FreightExportSingleViews, FreightExportPluralViews, FreightExportPluralViewsPlus, FreightReportStatisticsQueryViews, \
    FreightReportStatisticsSingleViews, FreightReportStatisticsPluralViews, FreightReportStatisticsPluralViewsPlus, \
    OrderReportStatisticsQueryViews

urlpatterns = [
    # 订单报表
    url(r'^orders-statement-query$', OrderReportQueryViews.as_view()),
    url(r'^orders-statement-export-single$', OrderExportSingleViews.as_view()),
    url(r'^orders-statement-export-plural$', OrderExportPluralViews.as_view()),
    url(r'^orders-statement-query-sum$', OrderReportStatisticsQueryViews.as_view()),
    url(r'^orders-statement-export-single-sum$', OrderReportStatisticsSingleViews.as_view()),
    url(r'^orders-statement-export-plural-sum$', OrderReportStatisticsPluralViews.as_view()),

    # 运单报表
    url(r'^freights-statement-query$', FreightReportQueryViews.as_view()),
    url(r'^freights-statement-export-single$', FreightExportSingleViews.as_view()),
    url(r'^freights-statement-export-plural$', FreightExportPluralViews.as_view()),
    url(r'^freights-statement-export-plural-plus$', FreightExportPluralViewsPlus.as_view()),
    url(r'^freights-statement-query-sum$', FreightReportStatisticsQueryViews.as_view()),
    url(r'^freights-statement-export-single-sum$', FreightReportStatisticsSingleViews.as_view()),
    url(r'^freights-statement-export-plural-sum$', FreightReportStatisticsPluralViews.as_view()),
    url(r'^freights-statement-export-plural-plus-sum$', FreightReportStatisticsPluralViewsPlus.as_view()),
]
