from enum import Enum


class VideoType(Enum):
    movie = "movie"
    cartoon = "cartoon"
    episode = "epsiode"
    variety = "variety"
    other = "other"


VideoType.movie.label = "电影"
VideoType.cartoon.label = "卡通"
VideoType.episode.label = "电视剧"
VideoType.variety.label = "综艺"
VideoType.other.label = "其它"


class FromType(Enum):
    youku = "youku"
    custom = "custom"


FromType.youku.label = "优酷"
FromType.custom.label = "自定义"


class NationalityType(Enum):
    china = "china"
    japan = "japan"
    america = "america"
    other = "other"


NationalityType.china.label = "中国"
NationalityType.japan.label = "日本"
NationalityType.america.label = "美国"
NationalityType.other.label = "其它"


class IdentityType(Enum):
    starring = "starring"
    costar = "costar"
    director = "director"


IdentityType.starring.label = "主演"
IdentityType.costar.label = "配角"
IdentityType.director.label = "导演"
