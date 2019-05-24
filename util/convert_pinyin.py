
def convert_chn_to_pinyin(myChn) -> str:
    'example: 上海 --> shanghai'
    from xpinyin import Pinyin
    return Pinyin().get_pinyin(myChn, splitter='')