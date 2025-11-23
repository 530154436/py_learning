# import requests
# from urllib import parse
#
# url = 'https://www.fxiaoke.com/FHH/EM1HORGBIZ/Organization/Employee/GetEmployeeByStopTimeStampRange'
#
# headers = {
#     # ':authority': 'www.fxiaoke.com',
#     # ':method': 'POST',
#     # ':path': '/FHH/EM1HORGBIZ/Organization/Employee/GetEmployeeByStopTimeStampRange',
#     # ':scheme': 'https',
#     'accept': 'application/json, text/javascript, */*; q=0.01',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh-TW;0.9,en;0.8',
#     'content-length': '60',
#     'content-type': 'application/json; charset=UTF-8',
#     'cookie': '_ga=GA1.2.1784059140.1590488046; guid=248fc908-fc6d-171f-d18e-717250799b27; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217250799b4f92e-0abdcdd4f525d8-f7d1d38-2073600-17250799b50ad3%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%7D; enterprise=gztdkj; lang=zh-CN; _gid=GA1.2.856640145.1590587799; Hm_lvt_06d5233541e92feb3cc8980700b1efa6=1590488046,1590587799; mirrorId=0000; Hm_lpvt_06d5233541e92feb3cc8980700b1efa6=1590588776; EPXId=caa5f30483ee4a84883476554d016eed; LoginId=LOGIN_ID_145414b7-9a22-4dea-a078-a0b1ac43a1b5; fs_token=PJ9ZPcDcCM4jE68sD2qqOMOnBM8qDJajOJOnCZSuPJTYP6Cs; FSAuthX=0G4rGp5tuG80003lvf01HA6zeIQzZ0Kg5RQSzbaBA1qyYGmdKTWVwcN53K6D3qvzRNOQ8mtOLH1yfJz4DIOIPPibHO03AazmuYFRyKmuK2uV9jkwg9AkitfCkpixPijUBzBEPNm1X3gOud2YiWrsqhUwzq0kyjHOweRboxC8Wn94pDrGOv56Nzf63rNEmHnVasfocwJB59ssFGkLbyrSYcpNNTkWyzPS2Kuu3ymq5v3gtO8p5Z6iHqT0yXSC3; FSAuthXC=0G4rGp5tuG80003lvf01HA6zeIQzZ0Kg5RQSzbaBA1qyYGmdKTWVwcN53K6D3qvzRNOQ8mtOLH1yfJz4DIOIPPibHO03AazmuYFRyKmuK2uV9jkwg9AkitfCkpixPijUBzBEPNm1X3gOud2YiWrsqhUwzq0kyjHOweRboxC8Wn94pDrGOv56Nzf63rNEmHnVasfocwJB59ssFGkLbyrSYcpNNTkWyzPS2Kuu3ymq5v3gtO8p5Z6iHqT0yXSC3; sso_token=b650f40f-50ba-4ea8-9304-f661b36c429e; JSESSIONID=3FA0DE0002FA6761817E4F1B73418E42',
#     'origin': 'https://www.fxiaoke.com',
#     'referer': 'https://www.fxiaoke.com/XV/Home/Index',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
#     'x-requested-with': 'XMLHttpRequest',
#     'x-trace-id': '84e016ff-a275-4162-b0b4-1e8b2c280505:14'
# }
#
# data ={
#     'traceId': 'E-E.gztdkj.1056-1355365',
#     '_fs_token': 'PJ9ZPcDcCM4jE68sD2qqOMOnBM8qDJajOJOnCZSuPJTYP6Cs'
# }
#
# resp = requests.post(url, data=data, headers=headers)
# print(resp)
# print(resp.json())

# import uuid
# _id = 'E-E.gztdkj.1056-84855650'
# for i in [uuid.NAMESPACE_DNS,uuid.NAMESPACE_OID, uuid.NAMESPACE_URL, uuid.NAMESPACE_X500]:
#     print(str(uuid.uuid3(i, _id)))
#     print(str(uuid.uuid5(i, _id)))

# print(uuid.uuid3(uuid.RESERVED_NCS, _id))

ua_set = set()
with open('/Users/zhengchubin/PycharmProjects/learn/python-tutorial/爬虫/ua_string.csv', errors='ignore') as f:
    for line in f:
        line = line.strip()
        ua_set.add(line)

with open('/Users/zhengchubin/PycharmProjects/learn/python-tutorial/爬虫/ua_string_unique.csv', mode='w') as f:
    for ua in ua_set:
        f.write(f'{ua}\n')

