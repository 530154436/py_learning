
PROVINCES_CN_ABBR = {
    "北京":"bj",
    "天津":"tj",
    "河北":"hb",
    "山西":"sx",
    "内蒙古":"nm",
    "辽宁":"ln",
    "吉林":"jl",
    "黑龙江":"hl",
    "上海":"sh",
    "江苏":"js",
    "浙江":"zj",
    "安徽":"ah",
    "福建":"fj",
    "江西":"jx",
    "山东":"sd",
    "广东":"gd",
    "广西":"gx",
    "海南":"hi",
    "河南":"ha",
    "湖北":"hb",
    "湖南":"hn",
    "重庆":"cq",
    "四川":"sc",
    "贵州":"gz",
    "云南":"yn",
    "西藏":"xz",
    "陕西":"sn",
    "甘肃":"gs",
    "青海":"qh",
    "宁夏":"nx",
    "新疆":"xj",
}

PROVINCES_ID = {
    "北京":"110000",
    "天津":"tj",
    "河北":"hb",
    "山西":"sx",
    "内蒙古":"nm",
    "辽宁":"ln",
    "吉林":"jl",
    "黑龙江":"hl",
    "上海":"sh",
    "江苏":"js",
    "浙江":"zj",
    "安徽":"ah",
    "福建":"fj",
    "江西":"jx",
    "山东":"sd",
    "广东":"gd",
    "广西":"gx",
    "海南":"hi",
    "河南":"ha",
    "湖北":"hb",
    "湖南":"hn",
    "重庆":"cq",
    "四川":"sc",
    "贵州":"gz",
    "云南":"yn",
    "西藏":"xz",
    "陕西":"sn",
    "甘肃":"gs",
    "青海":"qh",
    "宁夏":"nx",
    "新疆":"xj",
}

FIELDS_DEFAULT = {
    '_id': '',
    'pid': '',
    'from': '',
    'fromCN': '',
    'entName': '',              # 企业名称

    # 基本信息
    'basic':{
        'entLogo': '',          # 企业logo
        'telephone': '',        # 电话
        'email': '',            # 邮箱
        'website': '',          # 官网
        'describe': '',         # 简介
        'addr': '',             # 地址
    },

    # 工商注册信息
    'reg':{
        'regNo': '',            # 统一社会信用代码一般与纳税人识别号相同
        'taxNo': '',            # 纳税人识别号
        'orgNo': '',            # 组织机构代码
        'legalPerson': '',      # 法定代表人
        'openStatus': '',       # 经营状态
        'startDate': '',        # 成立日期
        'openTime': '',         # 营业期限
        'annualDate': '',       # 审核/年检日期
        'regCapital': '',       # 注册资本
        'realCapital': '',      # 实缴资本
        'entType': '',          # 企业类型
        'orgType': '',
        'industry': '',         # 所属行业
        'url': '',
        'paidinCapital': '',
        'prevEntName': '',      # 曾用名
        'district': '',         # 行政区划
        'licenseNumber': '',    # 工商注册号
        'scope': '',            # 经营范围
        'regAddr': '',          # 注册地址
        'authority': '',        # 登记机关
        'personLink': '',
        'compNum': 0,
        'compNumLink': '',
        'personId': ''
    }
}