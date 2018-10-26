from tornado_json.requesthandlers import APIHandler
from tornado_json.gen import coroutine
from tornado import gen
import tasks
from tornado.web import asynchronous
import tcelery
import time
tcelery.setup_nonblocking_producer()
from picture.sqldb import *

from picture.model import picture, Test

'''
# 验证和自动文档用
# @schema.validate(
#     input_schema={
#         "type": "object",
#         "properties": {
#             "title": {"type": "string"},
#             "body": {"type": "string"},
#             "index": {"type": "number"},
#         }
#     },
#     input_example={
#         "title": "Very Important Post-It Note",
#         "body": "Equally important message",
#         "index": 0
#     },
#     output_schema={
#         "type": "object",
#         "properties": {
#             "message": {"type": "string"}
#         }
#     },
#     output_example={
#         "message": "Very Important Post-It Note was posted."
#     },
# )
'''



#celery异步
class CEAsyncHandler(APIHandler):
    @asynchronous
    @coroutine
    def get(self):
        print(time.time())
        print('进入接口')
        # celery会print 参数
        tasks.sleep.apply_async(args=[1])
        self.success({"msg": "任务发布成功"})


class GenMultipleAsyncHandler(APIHandler):
    @asynchronous
    @coroutine
    def get(self):
        r1, r2 = yield [gen.Task(tasks.sleep.apply_async, args=[2]),
                        gen.Task(tasks.add.apply_async, args=[1, 2])]
        print(r1)
        print(r2)
        self.success({"msg": "任务发布成功"})

# json的异步 加了 callback
class Async(APIHandler):
    def hello(self, name, callback=None):
        callback({"msg": "Hello (asynchronous) world! My name is {}.".format(name)})

    @coroutine
    def get(self, name):
        res = yield gen.Task(self.hello, name)
        self.success(res)

#mysql的异步
#通用比较熟悉的peewee写法 不过需要在接口里面 有app的object
# obj = await self.application.objects.get(MyModel.select().where(MyModel.id==1))
# objects.create_or_get(PageBlock, key='title',text="Peewee is AWESOME with async!")
# objects.update(title)
class DbpeeweeHandler(APIHandler):
    async def get(self):
        obj_id = self.get_argument('id', None)
        try:
            obj = await self.application.objects.get(GameMediatag, title='本周五进行团建活动')
            print(obj.content)
            self.success({"msg": obj.content})
        except GameMediatag.DoesNotExist:
            raise self.fail("not exist")
        except Exception as e:
            print(e)
            raise self.fail("err")




#mongdb的异步
# picture.objects.limit(100).find_all()
# Test.objects.create(nameTest="foobar", boolTest=False, numberTest=123)
class ListPicHandler(APIHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        yield self.save_test()
        self.success({"msg":"保存成功"})

    @gen.coroutine
    def save_test(self):
        yield Test.objects.create(nameTest="foobar", boolTest=False, numberTest=123)



    def get(self):
        # queryset = await picture.objects.limit(100).find_all()
        queryset = picture.objects.limit(100).all()
        from picture.serializers import PictureSerializer
        serializer = PictureSerializer(queryset, many=True)
        data = serializer.data
        self.success(data)
        #在serializer 用 async 方法 去获取mongodb数据

        # queryset = self.filter_queryset(self.get_queryset())
        # tag1 = request.GET.get('taglevel1', 0)
        # tag2 = request.GET.get('taglevel2', 0)
        # tag3 = request.GET.get('taglevel3', 0)
        # accesstype = request.GET.get('accesstype', 0)
        # usetype = request.GET.get('usetype', 0)
        # gameid = request.GET.get("game", 0)
        # chapter_id = request.GET.get("chapter", 0)
        # badge = request.GET.get('badge', False)
        #
        # if int(accesstype) == Picture.PRIVATE:
        #     userid = self.request._user.id
        # else:
        #     userid = 0
        #
        # where = MongoQ(mask=True, usetype=int(usetype), userid=userid)
        #
        # if userid == 0:
        #     where &= MongoQ(accesstype=int(accesstype))
        #
        # if int(tag1) > 0:
        #     where &= MongoQ(taglevel1=int(tag1))
        # if int(tag2) > 0:
        #     where &= MongoQ(taglevel2=int(tag2))
        # if int(tag3) > 0:
        #     where &= MongoQ(taglevel3=int(tag3))
        #
        # if badge:
        #     # 过滤角标
        #     where &= MongoQ(badge=badge)
        #
        # if gameid:
        #     where &= MongoQ(game=int(gameid))
        #
        # if chapter_id:
        #     where &= MongoQ(chapter=chapter_id)
        #
        # queryset = queryset.filter(where).order_by("-created_time")
        # tag_id = request.GET.get("tag_id")  # id_list
        # if tag_id:
        #     tag_queryset = QuinTag.objects.filter()
        #     if tag_id != "all":
        #         tag_id_list = tag_id.split(",")
        #         tag_queryset = tag_queryset.filter(id__in=tag_id_list)
        #     if tag_queryset:
        #         l = tag_queryset.values_list("id", flat=True)
        #         for i in l:
        #             queryset = queryset.filter(quin_tag=i)
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = PictureSerializer(page, context={'request': request}, many=True)
        #     return self.get_paginated_response(serializer.data)
        # serializer = PictureSerializer(queryset, context={'request': request}, many=True)
        # return Response(serializer.data)
