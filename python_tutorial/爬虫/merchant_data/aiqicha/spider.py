# ----------------------------------------------------------------
# 爱企查
#
# 企业工商信息
# https://aiqicha.baidu.com/smart/basicAjax?pid=29453261288626

# 企业基本信息(电话、官网、简介)
# https://aiqicha.baidu.com/c/headinfoAjax?pid=29453261288626
#
# 注意: 爱企查一个关键词返回的数据总数有限制,即 p*s<=1000 条。
# ----------------------------------------------------------------

import time
import random
import json
import requests
from copy import deepcopy
from gsxt.constant import PROVINCES_CN_ABBR, FIELDS_DEFAULT
class AiQiChaSpider():
    def __init__(self):

        self._from = 'aiqicha'
        self._from_cn = '爱企查'

        self.URL = 'https://aiqicha.baidu.com/s/a?q={q_str}&t=0&p={p_num}&s=10&o=0'

        self.REG_INFO = 'https://aiqicha.baidu.com/smart/basicAjax?pid={pid}'
        self.BASIC_INFO = 'https://aiqicha.baidu.com/c/headinfoAjax?pid={pid}'

        self.HEADERS = {
            'Accept': "*/*",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
            'Accept-Encoding': "gzip, deflate, br",
            'Host': "aiqicha.baidu.com",
            'User-Agent': "",
            'Connection': "keep-alive",
        }

    def search(self, q:str, p:int, s:int=10, t:int=0):
        '''
        搜索接口
        示例: https://aiqicha.baidu.com/s/a?q=&t=0&p=10&s=10&o=0
        :param q: 查询关键词
        :param p: 页数
        :param s: 页大小 (不超过20)
        :param t: 类别(企业、老板)
        :return:
        '''
        url = self.URL.format(q_str=q, p_num=p)
        print(url)
        headers = deepcopy(self.HEADERS)
        headers['User-Agent'] = random.choice(xxx)
        rsp = requests.get(url, headers=self.HEADERS)
        if rsp.status_code==200:
            data = rsp.json()
            return data.get('data',{}).get('resultList', [])

    def clean(self, entries:list):
        '''
        清洗数据
        '''
        cleaned_data = []

        # 获取搜索列表
        for ent in entries:
            pid = ent.get('pid', '')
            entName = ent.get('entName', '')

            cleaned = deepcopy(FIELDS_DEFAULT)
            cleaned.update({
                '_id': f'{self._from}_{pid}',
                'pid': pid,
                'from': self._from,
                'fromCN': self._from_cn,
                'entName': entName
            })

            # 处理基本信息
            info_rsp = requests.get(self.BASIC_INFO.format(pid=pid), headers=self.HEADERS)
            if info_rsp.status_code == 200:
                info = info_rsp.json().get('data', {})
                dv = cleaned['basic']
                for k,v in dv.items():
                    dv[k] = info.get(k) if k in info else v

            # 处理工商信息
            info_rsp = requests.get(self.REG_INFO.format(pid=pid), headers=self.HEADERS)
            if info_rsp.status_code == 200:
                info = info_rsp.json().get('data', {}).get('dataInfo', {}).get('basic', {})
                dv = cleaned['reg']
                for k, v in dv.items():
                    dv[k] = info.get(k) if k in info else v

            cleaned_data.append(cleaned)
        return cleaned_data

    def get_by_province(self):
        for cn in PROVINCES_CN_ABBR.keys():
            for p in range(1,101):
                results = self.search(cn, p=p)
                for res in results:
                    print(json.dumps(res))

if __name__ == '__main__':
    # aiqicha = AiQiChaSpider()
    # aiqicha.get_by_province()
    ua = UserAgent()
    print(ua.random)



