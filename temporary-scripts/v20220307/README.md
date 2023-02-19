1. 环境配置
```shell
python -m pip install -r requirements.txt
```
2. 获取每一页的专家主页
```shell
python -u get_detail.py
```
下载到文件：details.txt
如果下载失败有异常，会把相应的链接存入errors.txt，手动保存到 htmls/目录下即可。
   
3. 下载每个专家的详情页
```shell
python -u get_detail_html.py
```
   
4. 抽取每个专家的信息、并结构化输出
```shell
python -u extract_info.py
```