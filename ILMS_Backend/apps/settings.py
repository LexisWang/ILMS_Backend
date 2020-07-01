CUS_RANK = 'KHJB'  # 客户级别常量(类别)
CHAN_CODE = 'FWQD'  # 服务渠道常量(类别)
PAY_TYPES = 'FKLX'  # 付款类型(类别)
GOOD_TYPES = 'HWLX'  # 货物类型(类别)
TRANS_COMP = 'HYGS'  # 货运公司
CUSTOMS = 'QINGGUAN'  # 清关
SUCCESS_CODE = 1000  # 成功码
FALSE_CODE = 1001  # 失败码
IMG_CODE_EXPIRE = 24 * 60 * 60  # 过期时间（过期时间为一天）

ORDER_STATUS_CHOICE = (  # 订单状态选项
    (1, '已入库'),
    (2, '运输中'),
    (3, '已签收'),
    (4, '已完成'),
    (5, '已终止'),
    (6, '异常'),
    (7, '已废弃')
)
FREIGHT_STATUS_CHOICE = (  # 运单状态选项
    (1, '运输中'),
    (2, '已签收'),
    (3, '已完成'),
    (4, '已终止'),
    (5, '已废弃')
)
GOOD_VIRTUAL_CHOICE = (  # 货物是否虚拟选项
    (0, '虚拟'),
    (1, '真实')
)
FUND_STATUS_CHOICE = (  # 款项状态选项
    (1, '未录入'),
    (2, '待结算'),
    (3, '部分结算'),
    (4, '已结算'),
    (5, '已冻结'),
    (6, '异常')
)
CUSTOMS_LEVEL_CHOICE = (  # 清关级别选项
    (0, '公司级'),
    (1, '业务级')
)
OTHER_FUND_TYPE_CHOICE = (  # 其他款项类型选项
    (0, '收款'),
    (1, '付款')
)
STATUS_USE_CHOICE = (  # 是否启用状选项
    (0, '禁用'),
    (1, '启用')
)
DATA_LEVEL_CHOICE = (  # 用户数据权限选项
    (1, '全部'),
    (2, '分部'),
    (3, '个人')
)
