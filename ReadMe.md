

anaconda search -t conda tornado-celery

完成了 celery的集成
和异步mysql 和mongo的连接
以及serializer的集成

其中tornado-celery的安装bug
The version of your tornado-celery is too low to support celery-4.1. You can install tornado-celery by "python setup.py install".


celery异步队列安装
docker run -d --hostname localhost --name rabbit-management --restart=always -p 15672:15672 -p 5672:5672 rabbitmq:3.6-management-alpine
访问：http://server-ip:15672  账号： guest 密码： guest

celery -A tasks worker --loglevel=info




mogndo

peewee

#data = YChome.select().where(YChome.id == id).get()

性能测试
sudo apt-get install apache2-utils
ab -n 10000 -c 100 http://127.0.0.1:8500/api/posts/query/