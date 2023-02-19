[TOC]
#### 部署
```shell
python -m pip install -r requirements.txt
```

#### 后端接口、前端调用
+ 后端WebSocket接口 ./application/ws_server.py
```shell
ws://192.168.1.102:5000/chat
```
+ 后端Web接口  ./application/app.py
```shell
http://192.168.1.102:5200/answer?question=章子怡和周润发共同演了什么电影？
```
+ 前端
```shell
./client  # CS
http://0.0.0.0:5200/  # 页面
```

+ Neo4j
```shell
# 启动图数据库服务器
./neo4j start -host 192.168.1.102

# 停止
./neo4j stop
```