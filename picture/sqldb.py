import peewee_async
from peewee import *

database = peewee_async.PooledMySQLDatabase(
    'nero', host='192.168.1.5', port=3306,
    user='dbadmin', password='123456', charset='utf8')


class BaseModel(Model):
    class Meta:
        database = database


class GameMediatag(BaseModel):
    cover = CharField()
    groupid = IntegerField()
    name = CharField()
    order = IntegerField()
    ref_count = IntegerField()
    typeid = IntegerField()
    usetype = IntegerField()

    class Meta:
        db_table = 'game_mediatag'


class GameQuinhighcategory(BaseModel):
    created_time = DateTimeField()
    name = CharField(unique=True)
    updated_time = DateTimeField()

    class Meta:
        db_table = 'game_quinhighcategory'


class GameQuincategory(BaseModel):
    created_time = DateTimeField()
    high = ForeignKeyField(db_column='high_id', null=True, rel_model=GameQuinhighcategory, to_field='id')
    name = CharField(unique=True)
    updated_time = DateTimeField()

    class Meta:
        db_table = 'game_quincategory'


class GameQuintag(BaseModel):
    category = ForeignKeyField(db_column='category_id', null=True, rel_model=GameQuincategory, to_field='id')
    created_time = DateTimeField()
    name = CharField(unique=True)
    updated_time = DateTimeField()

    class Meta:
        db_table = 'game_quintag'
