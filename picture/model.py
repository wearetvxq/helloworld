# from motorengine import Document, StringField, IntField, DecimalField, BooleanField, DateTimeField, ListField

from mongoengine import Document, StringField, IntField, DecimalField, BooleanField, DateTimeField, ListField
import datetime


class Test(Document):
    nameTest = StringField(required=True)
    numberTest = DecimalField(required=True)
    boolTest = BooleanField(required=True)


## 图片
class picture(Document):
    """
    taglevel1 对应 mediatag 中 groupid=1 的标签id
    taglevel2 对应 mediatag 中 groupid=2 的标签id
    taglevel3 对应 mediatag 中 groupid=3 的标签id
    userid = 0 为公用素材
    userid > 0 为私有素材
    """
    game = IntField(default=0)
    chapter = IntField(default=0)
    title = StringField(required=True)
    content = StringField(required=False)
    cdn_request_id = StringField(required=False)
    created_time = DateTimeField(default=datetime.datetime.now)
    size = IntField(default=0)
    uploadstatus = IntField(default=1)
    mask = BooleanField(default=True)
    taglevel1 = IntField(default=0)
    taglevel2 = IntField(default=0)
    taglevel3 = IntField(default=0)
    filetype = IntField(default=0)
    usetype = IntField(default=0)
    accesstype = IntField(default=0)
    userid = IntField(default=0)
    pic_type = IntField(default=0)  # 0 普通图 1 纸娃娃 2 差分图 3 可动素材 4 rule
    badge = StringField(default="0")
    extend_data = StringField(required=False)
    quin_tag = ListField(StringField(required=False))
    quin_high_category = IntField(default=0)
    meta = {
        'ordering': ['created_time'],
        'indexes': ['game', 'mask', 'userid', 'usetype', 'accesstype', 'taglevel1', 'taglevel2', 'taglevel3',
                    'pic_type', 'quin_tag', 'quin_high_category'],
    }


class Badge(Document):
    name = StringField(required=True)  # 角标显示名字
    mask = BooleanField(default=True)  # False为删除
    created_time = DateTimeField(default=datetime.datetime.now)
    meta = {'indexes': ['mask']}


import peewee_async
import peewee
