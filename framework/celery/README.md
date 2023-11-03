### Celery介绍
Celery 是一个异步任务队列，可以使用它在应用上下文之外执行任务。(即应用程序可能需要执行任何消耗资源的任务都可以交给任务队列，让应用程序自由和快速地响应客户端请求。)

+ Celery 通过消息代理(Broker)进行通信，通常使用代理在客户端和工作进程(Worker)之间进行调解。<br>
启动任务的过程：客户端向消息队列发送一条消息 => 消息代理将消息传递给工作进程 => 工作进程进行执行消息代理分配的任务
+ Celery 可以有多个工作进程（Worker）和消息代理（Broker），用来提高Celery的高可用性以及横向扩展能力。
+ Celery 是用 Python 编写的，但协议可以在任何语言中实现。<br>
可以通过公开一个HTTP端点并创建一个请求该端点的任务（Webhooks）来实现语言互操作性。

一个 Celery 安装有三个核心组件：

+ `Celery 客户端`<br>
用于发布后台作业。当与 Flask 一起工作的时候，客户端与 Flask 应用一起运行。
+ `Celery workers`<br>
运行后台作业的进程。<br>
Celery 支持本地和远程的 workers，因此可以在 Flask 服务器上启动一个单独的 worker，随后随着应用需求的增加而新增更多的 workers。
+ `消息代理`
客户端通过消息队列和 workers 进行通信，Celery 支持多种方式来实现这些队列。最常用的代理就是 RabbitMQ 和 Redis。

cd mainactivity/networkMedicine/celery_framework
celery -A celery_app worker --loglevel=info

celery -A mainactivity.networkMedicine.celery_framework.celery_app worker --loglevel=info 


### 参考引用
+ [在 Flask 中使用 Celery](http://www.pythondoc.com/flask-celery/first.html)
+ [flask-celery-example](https://github.com/miguelgrinberg/flask-celery-example)
+ [Celery 入门教程](https://blog.csdn.net/youzhouliu/article/details/124239709)
+ [Github-How to use pymysql for CELERY_RESULT_BACKEND](https://github.com/celery/celery/issues/3503)
