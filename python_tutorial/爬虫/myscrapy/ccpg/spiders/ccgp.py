# /usr/bin/env python3
# -*- coding:utf-8 -*-
import scrapy

from ccpg.item import MyItem

class CcgpSpiders(scrapy.Spider):
    name = "ccgp"
    start_time = "2016:01:01"
    end_time = "2016:12:31"
    kw = "水质"
    allowed_domains = ["ccgp.gov.cn"]
    url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&timeType=6&pppStatus=0&bidSort=0&pinMu=0&bidType=7&dbselect=bidx' \
                                          '&page_index={}' \
                                          '&kw={}' \
                                          '&start_time={}' \
                                          '&end_time={}'
    start_urls = []
    for page_index in range(1, 58):
        newURL = url.format(page_index,kw,start_time,end_time)
        start_urls.append(newURL)

    def parse(self, response):
        for href in response.xpath('//ul[@class="vT-srch-result-list-bid"]/li/a/@href'):
            url = href.extract()
            yield  scrapy.Request(url, callback=lambda response,url=url:self.parse_dir_contents(response,url))

    def parse_dir_contents(self, response, url):
        item = MyItem()
        item['url'] = url
        for row in response.xpath('//div[@class="table"]/table/tr'):
            td1 = row.xpath('./td[@class="title"]/text()').extract()
            td2 = row.xpath('./td[@colspan="3"]/text()').extract()

            if len(td1)>0 and '项目名称' in td1[0] and 'name' not in item:
                item['name'] = td2[0].encode('gbk', "ignore").decode('gbk')

            if len(td1)>0 and '中标金额' in td1[0] and 'amount' not in item:
                item['amount'] = td2[0].encode('gbk', "ignore").decode('gbk')

            if len(td1) > 0 and '采购单位' in td1[0] and 'fromCompany' not in item:
                item['fromCompany'] = td2[0].encode('gbk', "ignore").decode('gbk')

        stats = response.xpath('//div[@class="vF_detail_header"]/h2/text()').extract()
        if len(stats)>0 and '废标' in stats[0]:
            item['toCompany'] = '废标'
            # print(stats)
            yield item

        # 中标公司1
        # for u in response.xpath('//div[@id="generalArticleEditForm00080101_bidOrgDetailTDP"]/p/u'):
        for u in response.xpath('//div[contains(@id,"generalArticle")]/p/u'):

            toCompany = u.xpath('text()').extract()
            if len(toCompany) > 0 and 'toCompany' not in item:
                item['toCompany'] = toCompany[0].encode('gbk', "ignore").decode('gbk')
                break

        isFind = False
        # 中标公司2
        for div in response.xpath('//div[@class="vF_detail_content"]'):
            for td in div.xpath("./table/tbody/tr/td"):
                toCompany = td.xpath('text()').extract()
                toCompany2 = td.xpath('./table/tr/td').extract()
                # print(toCompany)

                if len(toCompany)<1:
                    toCompany = toCompany2

                if len(toCompany) > 0 and 'toCompany' not in item and  '公司' in toCompany[0]:
                    item['toCompany'] = toCompany[0].encode('gbk', "ignore").decode('gbk')
                    break

            flag = False
            for p in div.xpath("./p"):
                toCompany = p.xpath('text()').extract()
                toCompany2 = p.xpath('./span/font/text()').extract()
                if len(toCompany) < 1:
                    toCompany = toCompany2

                # print(toCompany)
                if len(toCompany) > 0 and '中标供应商' in toCompany[0] and not flag:
                    flag = True
                    continue
                if len(toCompany) > 0 and 'toCompany' not in item and flag and '公司' in toCompany[0]:
                    item['toCompany'] = toCompany[0].encode('gbk', "ignore").decode('gbk')
                    break

        for td in response.xpath('//table[@id="tabrow"]/tbody/tr/td'):
            toCompany = td.xpath('text()').extract()
            if len(toCompany) > 0 and 'toCompany' not in item and '公司' in toCompany[0]:
                item['toCompany'] = toCompany[0].encode('gbk', "ignore").decode('gbk')
                break
        yield item

    def isCompany(self):
        pass

