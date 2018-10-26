#!/usr/bin/env python

import sys

sys.path.append("../../")

import json
import tornado.ioloop
from tornado_json.routes import get_routes
from tornado_json.application import Application

import tcelery

from tornado.options import options, define

import tasks

from picture.sqldb import database
from tornado import ioloop
import peewee_async
# from motorengine import connect
from mongoengine import connect

import picture

define("port", type=int, default=8080, help="run server on the given port")


# celery
def handle_result(result):
    print(result.result)
    ioloop.IOLoop.instance().stop()


def call_task():
    tasks.add.apply_async(args=[1, 2], callback=handle_result)


# 自定义__init__函数
# class Application(tornado.web.Application):
#     def __init__(self, *args, **kwargs):
#         super(Application, self).__init__(*args, **kwargs)
#         self.db = torndb.Connection(**config.mysql_options)
#         self.redis = redis.StrictRedis(**config.redis_options)

def main():
    tornado.options.parse_command_line()
    routes = get_routes(picture)
    print("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2)
          )

    application = Application(routes=routes, settings={"debug": True, })

    application.objects = peewee_async.Manager(database)

    application.listen(8080)

    tcelery.setup_nonblocking_producer(on_ready=call_task)

    io_loop = tornado.ioloop.IOLoop.instance()

    # connect("nero_gate", host="192.168.1.5", port=27017, connect=False, io_loop=io_loop)  4
    # connect("nero_gate", host="192.168.1.5", port=27017, connect=False, io_loop=io_loop)  3
    connect("nero_gate", host="192.168.1.5", port=27017)

    io_loop.start()


if __name__ == '__main__':
    main()
