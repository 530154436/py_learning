from lxml import etree
import requests
from multiprocessing import Pool
import os

count = 0
data = set()
def get_meishitianxia_html(url):
    global count
    content = requests.get(url=url).content
    html = etree.HTML(content)
    nodes = html.xpath(r'//div[@class="detail"]')
    for node in nodes:
        dish = node.xpath(r'h2/a[@target="_blank"]/text()')
        if 2 < len(dish[0]) < 10:
            # print(dish[0].replace(' ',''))
            data.add(dish[0].replace(' ', ''))
        count = count + 1
        if count % 100 == 0:
            print(count)


def get_meishitianxia():
    '''
    美食天下-排行榜
    -当季最热、人气菜肴、明星菜谱、食神菜谱
    :return:
    '''
    urls = ['http://home.meishichina.com/show-top-type-recipe-order-quarter',
            'http://home.meishichina.com/show-top-type-recipe-order-pop',
            'http://home.meishichina.com/show-top-type-recipe-order-star',
            'http://home.meishichina.com/show-top-type-recipe-order-chef'
            ]
    for url in urls:
        get_meishitianxia_html(url=url + '.html')
        for page in range(2, 100):
            # print(page)
            get_meishitianxia_html(url + '-page-' + str(page) + '.html')


def get_meishitianxia_2():
    '''
    美食天下首页(更多)
    :return:
    '''
    global count
    for page in range(1, 50):
        response = requests.post(
            url='http://home.meishichina.com/ajax/ajax.php?ac=recipe&op=getMoreDiffStateRecipeList&classid=0&orderby=hot&page=' + str(
                page))
        dish_json = response.json()
        for data in dish_json['data']:
            print(data['title'] + '\n')
        count += 1
    print(count)

def get_meishijie_html(url):
    global count
    content = requests.get(url=url).content
    if content:
        html = etree.HTML(content)
        nodes = html.xpath(r'//div[@class="c1"]')
        for node in nodes:
            dish = node.xpath(r'strong/text()')
            if 2 < len(dish[0]) < 10:
                data.add(dish[0].replace(' ', ''))
                #print(dish[0])
                count = count + 1
                if(count %100 == 0):
                    print(url,str(count))

def get_meishijie():
    '''
    美食杰-中华菜系
    川菜 湘菜 粤菜 东北菜 鲁菜 浙菜 苏菜 清真菜 闽菜
    沪菜 京菜 湖北菜 徽菜 豫菜 西北菜 云贵菜 江西菜
    山西菜 广西菜 港台菜 其它菜

    美食杰-各地小吃
    四川小吃 广东小吃 北京小吃 陕西小吃 山东小吃 山西小吃
    湖南小吃 河南小吃 上海小吃 江苏小吃 湖北小吃 重庆小吃
    天津小吃 河北小吃 浙江小吃 新疆小吃 江西小吃 福建小吃
    广西小吃 云南小吃 辽宁小吃 吉林小吃 贵州小吃 安徽小吃
    台湾小吃 甘肃小吃 香港小吃 蒙古小吃 宁夏小吃 青海小吃
    海南小吃 西藏小吃 成都小吃 黑龙江小吃

    美食杰-家常菜谱
    家常菜 私家菜 凉菜 海鲜 热菜 汤粥 素食

    美食杰-外国菜谱
    韩国料理 日本料理 西餐面点 法国菜 意大利餐 美国家常菜 东南亚菜 墨西哥菜 澳大利亚 菜其他国家
    :return:
    '''
    zhonghuacaixi_id = [41,44,43,53,42,46,47,56,45,50,49,52,48,51,54,55,269,268,385,154,155]
    xiaochi_id = [101,105,78,91,81,84,97,98,83,85,96,100,79,80,86,92,99,88,
                  106,107,102,90,89,103,87,110,94,109,82,93,95,108,104,344]
    jiachangcai_id = [270,271,5,75,6,7,74]
    waiguocai_id = [64,63,156,67,66,65,69,68,70,71]

    for id in zhonghuacaixi_id + xiaochi_id + jiachangcai_id + waiguocai_id:
        url = 'http://www.meishij.net/list.php?sortby=renqi&lm=' + str(id)
        get_meishijie_html(url=url)
        for page in range(2, 56):
            get_meishijie_html(url + '&page=' + str(page))

def get_douguo_html(url):
    global count
    global data
    content = requests.get(url=url).content
    if content:
        html = etree.HTML(content)
        nodes = html.xpath(r'//li/a[@target="_blank"]')
        for node in nodes:
            dish = node.xpath(r'text()')
            if 2 < len(dish[0]) < 10:
                data.add(dish[0].replace(' ', ''))
                print(dish[0])
                count = count + 1
                if(count %100 == 0):
                    print(url,str(count))

def get_douguo():
    '''
    豆果网部分食谱
    http://www.douguo.com/allrecipes/
    :return:
    '''
    url = 'http://www.douguo.com/allrecipes/'
    get_douguo_html(url=url)

def write_data(file):
    global data
    with open(file, 'w') as w:
        for title in data:
            w.write(title + '\n')
            w.flush()
    print(count)

if __name__ == '__main__':
    # get_meishitianxia()
    # get_meishitianxia_2()
    # get_meishijie()
    get_douguo()
    write_data('/test/corpus_1/dish/dic/raw/dish_douguo.txt')