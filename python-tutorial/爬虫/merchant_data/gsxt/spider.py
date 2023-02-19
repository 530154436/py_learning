# ----------------------------------------------------------------
# http://www.gsxt.gov.cn/index.html
# 国家企业信用信息公示系统-较难
#
# https://www.pythonf.cn/read/171496
#
# ----------------------------------------------------------------
from merchant_data.gsxt.constant import PROVINCES_CN_ABBR
import requests

class GSXTSpider():
    def __init__(self):
        pass

    def crawl(self):
        for province,cn_abbr in PROVINCES_CN_ABBR.items():
            host = f'{cn_abbr}.gsxt.gov.cn'
            url = f'http://{host}/index.html'
            headers = {
                'Accept': "*/*",
                'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
                'Accept-Encoding': "gzip, deflate, br",
                'Host': host,
                'Referer': url,
                'X-Requested-With': 'XMLHttpRequest',
                'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                'connection': "keep-alive",
            }

            rsp = requests.get(url)
            print(rsp)

            break

    def get_province_id(self):
        pass

    def get_hot_search_list(self):
        pass

if __name__ == '__main__':
    gsxt = GSXTSpider()
    gsxt.crawl()
#     gsxt.get_province_id()

