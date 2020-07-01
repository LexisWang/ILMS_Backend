from pandas import DataFrame
from rest_pandas import PandasSerializer
from rest_framework import serializers


# 订单报表序列化器
class OrderStatementSerial(serializers.Serializer):
    trans_code = serializers.CharField()
    customer = serializers.StringRelatedField()
    goods_name = serializers.CharField()
    goods_name_en = serializers.CharField()
    good_type = serializers.StringRelatedField()
    order_status = serializers.CharField(source='get_order_status_display')
    channel = serializers.StringRelatedField()
    salesman = serializers.CharField()
    service = serializers.CharField()
    operators = serializers.StringRelatedField(many=True)
    destination = serializers.SerializerMethodField()
    receiver = serializers.StringRelatedField()
    order_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    price_w = serializers.FloatField()
    weight = serializers.FloatField()
    volume = serializers.FloatField()

    def get_destination(self, obj):
        return '/'.join([obj.receiver.county.name, obj.receiver.city.name])


# 订单报表 'pandas' 序列化器
class OrderPandasSerializer(PandasSerializer):
    def transform_dataframe(self, dataframe):

        return super().transform_dataframe(dataframe)

    def get_dataframe(self, data):
        dataframe = DataFrame(data)
        dataframe.columns = ['转单号', '所属客户', '货物名称', '货物品名', '货物类型', '订单状态', '所属渠道',
                             '业务员', '客服专员', '操作员', '目的地', '收货方', '订单时间', '价格重量', '重量', '体积']
        dataframe.index.name = '序号'
        return dataframe


if __name__ == '__main__':
    pass
