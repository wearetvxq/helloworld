from picture.model import picture, Badge
from picture.sqldb import GameMediatag, GameQuintag

MIN = 0
PIC_CDN_BROWSE = 'https://image.iqing.in'
PLAY_ROLE_CSS = ''
PLAY_BGP_CSS = ''

from serpy import Serializer, StrField, MethodField



#model的字段 serpy.Field(attr='super_long_thing')
#model的静态方法 serpy.Field(call=True)



class PictureSerializer(Serializer):
    fields = (
        'id', 'game', 'title', 'link', 'size', 'type', 'usetype', 'taglevel1', 'taglevel2', 'taglevel3',
        'created_time', 'quin_tag',
        'pic_type', 'badge', 'extend_data')

    # id = IntField(attr='id')
    title = MethodField()
    link = MethodField()
    taglevel1 = MethodField()
    taglevel2 = MethodField()
    taglevel3 = MethodField()
    created_time = MethodField()
    # size = IntField(attr='_id')
    type = MethodField()
    usetype = MethodField()
    # game = IntField(attr='_id')
    # pic_type = IntField(attr='_id')
    extend_data = StrField(required=True)
    badge = MethodField()
    quin_tag = MethodField()

    async def get_mongo_Badge(self,id):
        return await Badge.objects.filter(id=id).find_all()[0]

    def get_quin_category(self, instance):
        if instance.category:
            return {"category_id": instance.category.id, "category_name": instance.category.name}
        return None

    def get_quin_high_category(self, instance):
        if instance.category:
            if instance.category.high:
                return {"high_id": instance.category.high.id, "high_name": instance.category.high.name}
        return None

    def get_created_time(self, obj):
        return obj.created_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_badge(self, obj):
        if obj.badge == "0":
            return ""
        else:
            try:
                return Badge.objects.filter(id=obj.id).find_all()[0]
            except Exception:
                return ""

    def get_id(self, obj):
        return str(obj.id)

    def get_title(self, obj):
        return obj.title

    def get_link(self, obj):
        if obj.usetype == 1:  # 查一下 应该是1
            return '%s%s%s' % (PIC_CDN_BROWSE, obj.content.startswith('/')
                               and obj.content or '/%s' % obj.content, PLAY_BGP_CSS)
        else:
            return '%s%s%s' % (PIC_CDN_BROWSE, obj.content.startswith('/')
                               and obj.content or '/%s' % obj.content, PLAY_ROLE_CSS)

    def get_type(self, obj):
        return ('webp', 'jpg', 'png', 'gif', 'bmp',)[obj.filetype]

    def get_usetype(self, obj):
        return ('bgp', 'role', "avatar", "item")[obj.usetype]

    def get_taglevel1(self, obj):
        if obj.taglevel1 > 0:
            taginfo = {}
            tag = GameMediatag.select().where(GameMediatag.id == obj.taglevel1).get()
            taginfo["id"] = tag.id
            taginfo["name"] = tag.name
            return taginfo
        else:
            return None

    def get_taglevel2(self, obj):
        if obj.taglevel2 > 0:
            taginfo = {}
            tag = GameMediatag.select().where(GameMediatag.id == obj.taglevel2).get()
            taginfo["id"] = tag.id
            taginfo["name"] = tag.name
            return taginfo
        else:
            return None

    def get_taglevel3(self, obj):
        if obj.taglevel3 > 0:
            taginfo = {}
            tag = GameMediatag.select().where(GameMediatag.id == obj.taglevel3).get()
            taginfo["id"] = tag.id
            taginfo["name"] = tag.name
            return taginfo
        else:
            return None

    def get_quin_tag(self, instance):
        result = []
        if instance.quin_tag:
            for tag in instance.quin_tag:
                try:
                    tag = GameQuintag.select().where(GameQuintag.id == tag).get()
                except GameQuintag.DoesNotExist:
                    continue
                tag_dict = {
                    "id": tag.id,
                    "name": tag.name,
                    "category": None,
                    "high": None}
                if tag.category:
                    tag_dict["category"] = {
                        "id": tag.category.id,
                        "name": tag.category.name}
                    if tag.category.high:
                        tag_dict["high"] = {
                            "id": tag.category.high.id,
                            "name": tag.category.high.name}
                result.append(tag_dict)
        return result



