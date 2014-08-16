# -*- coding:utf-8 -*-

data = [
    {"cn":u"未知",    "en":"Unknown",  "jp":u"不詳",    "cap":u"未知",    "loc":u"未知",  "isl":u"未知",  "iso":"",     "id":0},
    {"cn":u"北海道",  "en":"Hokkaido", "jp":u"北海道",  "cap":u"札幌市",  "loc":u"北海道","isl":u"北海道","iso":"JP-01","id":1},
    {"cn":u"青森县",  "en":"Aomori",   "jp":u"青森県",  "cap":u"青森市",  "loc":u"东北",  "isl":u"本州",  "iso":"JP-02","id":2},
    {"cn":u"岩手县",  "en":"Iwate",    "jp":u"岩手県",  "cap":u"盛冈市",  "loc":u"东北",  "isl":u"本州",  "iso":"JP-03","id":3},
    {"cn":u"宫城县",  "en":"Miyagi",   "jp":u"宮城県",  "cap":u"仙台市",  "loc":u"东北",  "isl":u"本州",  "iso":"JP-04","id":4},
    {"cn":u"秋田县",  "en":"Akita",    "jp":u"秋田県",  "cap":u"秋田市",  "loc":u"东北",  "isl":u"本州",  "iso":"JP-05","id":5},
    {"cn":u"山形县",  "en":"Yamagata", "jp":u"山形県",  "cap":u"山形市",  "loc":u"东北",  "isl":u"本州",  "iso":"JP-06","id":6},
    {"cn":u"福岛县",  "en":"Fukushima","jp":u"福島県",  "cap":u"福岛市",  "loc":u"东北",  "isl":u"本州",  "iso":"JP-07","id":7},
    {"cn":u"茨城县",  "en":"Ibaraki",  "jp":u"茨城県",  "cap":u"水户市",  "loc":u"关东",  "isl":u"本州",  "iso":"JP-08","id":8},
    {"cn":u"栃木县",  "en":"Tochigi",  "jp":u"栃木県",  "cap":u"宇都宫市","loc":u"关东",  "isl":u"本州",  "iso":"JP-09","id":9},
    {"cn":u"群马县",  "en":"Gunma",    "jp":u"群馬県",  "cap":u"前桥市",  "loc":u"关东",  "isl":u"本州",  "iso":"JP-10","id":10},
    {"cn":u"埼玉县",  "en":"Saitama",  "jp":u"埼玉県",  "cap":u"埼玉市",  "loc":u"关东",  "isl":u"本州",  "iso":"JP-11","id":11},
    {"cn":u"千叶县",  "en":"Chiba",    "jp":u"千葉県",  "cap":u"千叶市",  "loc":u"关东",  "isl":u"本州",  "iso":"JP-12","id":12},
    {"cn":u"东京都",  "en":"Tokyo",    "jp":u"東京都",  "cap":u"新宿区",  "loc":u"关东",  "isl":u"本州",  "iso":"JP-13","id":13},
    {"cn":u"神奈川县","en":"Kanagawa", "jp":u"神奈川県","cap":u"横滨市",  "loc":u"关东",  "isl":u"本州",  "iso":"JP-14","id":14},
    {"cn":u"新潟县",  "en":"Niigata",  "jp":u"新潟県",  "cap":u"新潟市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-15","id":15},
    {"cn":u"富山县",  "en":"Toyama",   "jp":u"富山県",  "cap":u"富山市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-16","id":16},
    {"cn":u"石川县",  "en":"Ishikawa", "jp":u"石川県",  "cap":u"金泽市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-17","id":17},
    {"cn":u"福井县",  "en":"Fukui",    "jp":u"福井県",  "cap":u"福井市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-18","id":18},
    {"cn":u"山梨县",  "en":"Yamanashi","jp":u"山梨県",  "cap":u"甲府市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-19","id":19},
    {"cn":u"长野县",  "en":"Nagano",   "jp":u"長野県",  "cap":u"长野市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-20","id":20},
    {"cn":u"岐阜县",  "en":"Gifu",     "jp":u"岐阜県",  "cap":u"岐阜市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-21","id":21},
    {"cn":u"静冈县",  "en":"Shizuoka", "jp":u"静岡県",  "cap":u"静冈市",  "loc":u"中部",  "isl":u"本州",  "iso":"JP-22","id":22},
    {"cn":u"爱知县",  "en":"Aichi",    "jp":u"愛知県",  "cap":u"名古屋市","loc":u"中部",  "isl":u"本州",  "iso":"JP-23","id":23},
    {"cn":u"三重县",  "en":"Mie",      "jp":u"三重県",  "cap":u"津市",    "loc":u"近畿",  "isl":u"本州",  "iso":"JP-24","id":24},
    {"cn":u"滋贺县",  "en":"Shiga",    "jp":u"滋賀県",  "cap":u"大津市",  "loc":u"近畿",  "isl":u"本州",  "iso":"JP-25","id":25},
    {"cn":u"京都府",  "en":"Kyoto",    "jp":u"京都府",  "cap":u"京都市",  "loc":u"近畿",  "isl":u"本州",  "iso":"JP-26","id":26},
    {"cn":u"大阪府",  "en":"Osaka",    "jp":u"大阪府",  "cap":u"大阪市",  "loc":u"近畿",  "isl":u"本州",  "iso":"JP-27","id":27},
    {"cn":u"兵库县",  "en":"Hyogo",    "jp":u"兵庫県",  "cap":u"神户市",  "loc":u"近畿",  "isl":u"本州",  "iso":"JP-28","id":28},
    {"cn":u"奈良县",  "en":"Nara",     "jp":u"奈良県",  "cap":u"奈良市",  "loc":u"近畿",  "isl":u"本州",  "iso":"JP-29","id":29},
    {"cn":u"和歌山县","en":"Wakayama", "jp":u"和歌山県","cap":u"和歌山市","loc":u"近畿",  "isl":u"本州",  "iso":"JP-30","id":30},
    {"cn":u"鸟取县",  "en":"Tottori",  "jp":u"鳥取県",  "cap":u"鸟取市",  "loc":u"中国",  "isl":u"本州",  "iso":"JP-31","id":31},
    {"cn":u"岛根县",  "en":"Shimane",  "jp":u"島根県",  "cap":u"松江市",  "loc":u"中国",  "isl":u"本州",  "iso":"JP-32","id":32},
    {"cn":u"冈山县",  "en":"Okayama",  "jp":u"岡山県",  "cap":u"冈山市",  "loc":u"中国",  "isl":u"本州",  "iso":"JP-33","id":33},
    {"cn":u"广岛县",  "en":"Hiroshima","jp":u"広島県",  "cap":u"广岛市",  "loc":u"中国",  "isl":u"本州",  "iso":"JP-34","id":34},
    {"cn":u"山口县",  "en":"Yamaguchi","jp":u"山口県",  "cap":u"山口市",  "loc":u"中国",  "isl":u"本州",  "iso":"JP-35","id":35},
    {"cn":u"德岛县",  "en":"Tokushima","jp":u"徳島県",  "cap":u"德岛市",  "loc":u"四国",  "isl":u"四国",  "iso":"JP-36","id":36},
    {"cn":u"香川县",  "en":"Kagawa",   "jp":u"香川県",  "cap":u"高松市",  "loc":u"四国",  "isl":u"四国",  "iso":"JP-37","id":37},
    {"cn":u"爱媛县",  "en":"Ehime",    "jp":u"愛媛県",  "cap":u"松山市",  "loc":u"四国",  "isl":u"四国",  "iso":"JP-38","id":38},
    {"cn":u"高知县",  "en":"Kochi",    "jp":u"高知県",  "cap":u"高知市",  "loc":u"四国",  "isl":u"四国",  "iso":"JP-39","id":39},
    {"cn":u"福冈县",  "en":"Fukuoka",  "jp":u"福岡県",  "cap":u"福冈市",  "loc":u"九州",  "isl":u"九州",  "iso":"JP-40","id":40},
    {"cn":u"佐贺县",  "en":"Saga",     "jp":u"佐賀県",  "cap":u"佐贺市",  "loc":u"九州",  "isl":u"九州",  "iso":"JP-41","id":41},
    {"cn":u"长崎县",  "en":"Nagasaki", "jp":u"長崎県",  "cap":u"长崎市",  "loc":u"九州",  "isl":u"九州",  "iso":"JP-42","id":42},
    {"cn":u"熊本县",  "en":"Kumamoto", "jp":u"熊本県",  "cap":u"熊本市",  "loc":u"九州",  "isl":u"九州",  "iso":"JP-43","id":43},
    {"cn":u"大分县",  "en":"Oita",     "jp":u"大分県",  "cap":u"大分市",  "loc":u"九州",  "isl":u"九州",  "iso":"JP-44","id":44},
    {"cn":u"宫崎县",  "en":"Miyazaki", "jp":u"宮崎県",  "cap":u"宫崎市",  "loc":u"九州",  "isl":u"九州",  "iso":"JP-45","id":45},
    {"cn":u"鹿儿岛县","en":"Kagoshima","jp":u"鹿児島県","cap":u"鹿儿岛市","loc":u"九州",  "isl":u"九州",  "iso":"JP-46","id":46},
    {"cn":u"冲绳县",  "en":"Okinawa",  "jp":u"沖縄県",  "cap":u"那霸市",  "loc":u"冲绳",  "isl":u"冲绳",  "iso":"JP-47","id":47},
]

def get(id, k = 'cn'):
    if id:
        return data[id][k]
    else:
        return data[0][k]


def getIdByJp(jpStr):
    for dic in data[1:]:
        if jpStr in dic['jp']:
            return dic['id']
    return None

def searchIdByCn(cnStr):
    res = []
    for dic in data[1:]:
        if cnStr in dic['cn']:
            res.append(dic['id'])
            pass
        pass
    return res

def searchIdByJp(jpStr):
    res = []
    for dic in data[1:]:
        if jpStr in dic['jp']:
            res.append(dic['id'])
            pass
        pass
    return res
def searchIdByEn(enStr):
    for dic in data[1:]:
        if enStr == dic['en'].lower():
            return dic['id']
            pass
        pass
    return None

def toJson():
    pass
