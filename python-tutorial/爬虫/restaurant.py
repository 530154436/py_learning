from lxml import etree
import requests
from multiprocessing import Pool
import os

count = 0
data = set()
def get_maigou_html(url):
    global count
    content = requests.get(url=url).text
    #print(content)
    result = []
    if content:
        html = etree.HTML(content)
        nodes = html.xpath(r'//a[@class="dhidden"]')
        for node in nodes:
            name = node.xpath(r'text()')
            data.add(name[0].replace(' ', ''))
            print(name[0])
            count = count + 1
            if(count %100 == 0):
                print(url,str(count))
            result.append(name[0])
        return result

def get_maigou():
    '''
    买购网-餐饮品牌
    咖啡厅 中餐/聚餐宴请 火锅 餐饮连锁 面点/面食 烧烤/烤鱼/烤肉 外国菜 烤鸭 茶餐厅 西餐-牛排
    :return:
    '''
    cat_id = [2987,1318,1321,1811,2192,1271,3642,1250,4957,4944]

    for id in cat_id:
        url = 'http://10.maigoo.com/search/?catid='+str(id)+'&action=ajax&getac=brand'
        for page in range(2, 100):
            print(page)
            result = get_maigou_html(url + '&page=' + str(page))
            if not result:
                break

def write_data(file):
    global data
    with open(file, 'w') as w:
        for title in data:
            w.write(title + '\n')
            w.flush()
    print(count)

if __name__ == '__main__':
    get_maigou()
    write_data('/test/corpus_1/dish/dic/raw/res_brand.txt')