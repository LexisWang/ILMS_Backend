from pandas import DataFrame
from rest_pandas import PandasSerializer
from rest_framework import serializers


# 运单报表序列化器
class FreightStatementSerial(serializers.Serializer):
    freight_code = serializers.CharField()
    trans_company = serializers.StringRelatedField()
    mid_company = serializers.StringRelatedField()
    freight_status = serializers.CharField(source='get_freight_status_display')
    channel = serializers.StringRelatedField()
    pack_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    mid_port = serializers.CharField
    price_w = serializers.FloatField()
    weight = serializers.FloatField()
    volume = serializers.FloatField()


# 运单报表 'pandas' 序列化器
class FreightPandasSerializer(PandasSerializer):
    def transform_dataframe(self, dataframe):

        return super().transform_dataframe(dataframe)

    def get_dataframe(self, data):
        dataframe = DataFrame(data)
        dataframe.columns = ['运单号', '货运公司', '中港公司', '运单状态', '货运渠道', '运单时间', '中转站', '实际重量(kg)', '重量(kg)', '体积(cm3)']
        dataframe.index.name = '序号'
        return dataframe


if __name__ == '__main__':
    pass
