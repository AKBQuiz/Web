# -*- coding: utf-8 -*-
import urllib2,os,re,datetime
from urllib import urlencode, quote
from lxml import etree


GROUPS = ('akb', 'ske', 'nmb', 'hkt', )
todaystr = datetime.date.today().strftime("%y%m")

RE_MIME = re.compile(r"Content-Type: ([\w\\/]+)\r?\n")
RE_DATE = re.compile(ur"(\d{4}) *年 *(\d{1,2}) *月 *(\d{1,2}) *日")
RE_CONCURRENT = re.compile(ur"([A-Za-z]{3}\d{2}) *チーム([A-Za-z ]+) */ *([A-Za-z]{3}\d{2}) *チーム *([A-Za-z0-9 ]+)兼任")

URL_START = {
    'akb':'http://www.akb48.co.jp/about/members/',
    'ske':'http://www.ske48.co.jp/profile/list.php',
    'nmb':'http://www.nmb48.com/member/',
    'hkt':'http://www.hkt48.jp/profile/',
    'snh':'http://www.snh48.com/member_list.html',
}
XPATH_START = {
    'akb':"//div[@class='team_list_box cnr6']/ul/li/a/@href",
    'ske':"//ul[@class='list clearfix']/li/dl/dd/h3/a/@href",
    'nmb':"//div[@class='memberList']/ul[@class='team-section clearfix']/li/dl/dd",
    'hkt':"//div[@class='profile_list']/ul[@class='cf']/li/a/@href",
    'snh':"//div[@class='ny_k_np']/div[@class='ny_tn']/div/div[1]/a/@href",
}
JAP_TO_KEY = {
    u"生年月日"        :"birthday_str",
    u"ニックネーム"    :"nick",
    u"血液型"          :"bloodtype",
    u"出身地"          :"hometown",
    u"身長"            :"height",
    u"キャッチフレーズ":"catchphrase",
    u"特技"            :"stunt",
    u"将来の夢"        :"dream",
    u"好きな食べ物"    :"favfood",
    u"好きな言葉"      :"favquote",
    u"一言メッセージ"  :"msg",
    u"趣味"            :"hobby",
    u"チャームポイント":"charm",
}

def str2date(datetimestr):
    m = RE_DATE.match(datetimestr)
    if m:
        g = m.groups()
        return datetime.date(int(g[0]),int(g[1]),int(g[2]))
    return None

def grabHTML(url):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36')
        response = urllib2.urlopen(request,timeout = 10)
        code = response.getcode()
        if not 200 <= code <= 300 :
            print 'error : code [ %d ]' % code
            return None
        html = response.read()
        return html
    except Exception, e:
        print e

def doXPath(url, xpathdict, retry = 5, savehtml = False, filename = 'test.html'):
    ''' Get html form url and do a series of xpath opt in xpathdict then return results as a dict
    '''
    for x in xrange(retry):
        html = grabHTML(url)
        if html:
            print 'Get html from "%s" success!' % (url)
            break
        else:
            if x < 4:
                print 'Get html from "%s" fail, retrying: %d' % (url, x + 1)
            else:
                print 'Get html from "%s" fail!' % (url)
                return None

    if savehtml:
        f = codecs.open(filename,'wb+','utf-8')
        f.write(html.decode('utf-8'))
        f.close()

    page = etree.HTML(html)
    return {k:page.xpath(xpathdict[k]) for k in xpathdict}

def startQueue(group):
    from sae.taskqueue import TaskQueue,Task
    if group in GROUPS:
        for x in xrange(5):
            html = grabHTML(URL_START[group])
            if html:
                print 'Get html from "%s" success!' % (URL_START[group])
                break
            else:
                if x < 4:
                    print 'Get html from "%s" fail, retrying: %d' % (URL_START[group], x + 1)
                else:
                    print 'Get html from "%s" fail!' % (URL_START[group])
                    return None
        page = etree.HTML(html)
        tq = TaskQueue('crawler')
        if group == 'nmb':
            res = page.xpath(XPATH_START[group])
            paramlist = []
            for r in res:
                para = {'u' : r.find('h4/a').attrib['href'],'s':'qiniu'}
                extra = r.find("p/span")
                if extra:
                    para['e'] = ''.join(extra.itertext())
                    pass
                tq.add(Task('/crawler/info/%s/handler/?%s' % (group,urlencode(para))))
            return '%d tasks added' % len(res)
        if group == 'ske':
            root = page.xpath("//div[@id='sectionMain']")[0]
            count = 0
            para = {'s':'qiniu'}
            for e in root.getchildren():
                if e.tag == "span":
                    para['e'] = e.find("h3").text.encode('utf-8')
                elif e.tag == "ul":
                    for a in e.findall("li/dl/dd/h3/a"):
                        para['u'] = a.attrib.get('href')
                        tq.add(Task('/crawler/info/%s/handler/?%s' % (group,urlencode(para))))
                        count += 1
                    pass
            return '%d tasks added' % count
        else:
            res = page.xpath(XPATH_START[group])
            if res:
                tl = [Task('crawler/info/%s/handler/?%s' % (group,urlencode({'u':r, 's':'qiniu'}))) for r in res]
                tq.add(tl)
            return '%d tasks added' % len(res)
    else:
        return None
    pass

def taskHandler(group,url,saveto,extra):
    if group =='akb':
        return akbmember(url,saveto,extra)
    elif group =='ske':
        return skemember(url,saveto,extra)
    elif group =='nmb':
        return nmbmember(url,saveto,extra)
    elif group =='hkt':
        return hktmember(url,saveto,extra)
    # elif group =='snh':
    #     return snhmember(url,saveto)
    else:
        return None
    pass

def grabInfo(url,
    xpathdic,
    info_urlfactory = None,
    avatar_urlfactory = None,
    prefix = '',
    saveto = 'no'):
    """获取url的html，并应用xpathdic的dict，保存成员图片到指定的位置"""
    if info_urlfactory:
        url = info_urlfactory(url)
    else:
        url = url

    info = doXPath(url, xpathdic)
    if info:
        for k in info:
            if info[k]:
                if len(info[k]) > 1:
                    info[k] = [''.join(e.itertext()) for e in info[k]]
                else :
                    info[k] = info[k][0]
                    if isinstance(info[k],etree._Element):
                        info[k] = ''.join(info[k].itertext())
                        pass
            else :
                info[k] = None

        info['name'] = info['name'].replace(u'　','')
        info['name'] = info['name'].replace(' ','')

        if info['avatar_src']:
            if avatar_urlfactory:
                info['avatar_src'] = avatar_urlfactory(url,info['avatar_src'])
            if saveto == 'qiniu':
                from hashlib import md5
                filename = md5((u"%s-%s" % (info['name'], todaystr)).encode('utf-8')).hexdigest()
                filename = "%s/%s" % (prefix, filename)
                info["avatar"] = qiniufetch(info['avatar_src'],'akb-member',filename)
            elif saveto == 'storage':
                filename = "%s/%s-%s.%s" % (prefix, info['name'], todaystr, info['avatar_src'].split('.')[-1])
                info["avatar"] = retrieve(info['avatar_src'],'avatar',filename)
    return info

def retrieve(url, bucket, filename, retry = 5):
    """保存url的图片到storage"""
    from sae.storage import Bucket
    for x in xrange(1,6):
        try:
            img = urllib2.urlopen(url)
            b = Bucket(bucket)
            mime = RE_MIME.search(str(img.info()))
            if mime:
                mime = mime.groups()[0]
            b.put_object(filename,img.read(),mime)
            print 'Save "%s" to "%s/%s", MimeType:"%s"' % (url,bucket,filename,mime)
            return "http://akbquiz-%s.stor.sinaapp.com/" % (bucket,quote(filename.encode('utf-8')))
        except Exception, e:
            print 'Save image file "%s" failed, retrying: %d. (%s)' %(url, x, e)
        pass
    return None

def qiniufetch(url,bucket,filename):
    """调用七牛的fetch API 将url的图片存储到七牛"""
    from base64 import urlsafe_b64encode as b64e
    from qiniu.auth import digest
    access_key = "Mm3eTLInPMoWnh2uBpZ8MarSQw1esZdaCmQgqapu"
    secret_key = "3msmgC6ZISF9tjJcXsYZcr10tOjG13fX0-pdtMKb"

    encoded_url = b64e(url)
    dest_entry = "%s:%s" % (bucket, filename)
    encoded_entry = b64e(dest_entry.encode('utf-8'))

    api_host = "iovip.qbox.me"
    api_path = "/fetch/%s/to/%s" % (encoded_url, encoded_entry)

    mac = digest.Mac(access=access_key, secret=secret_key)
    client = digest.Client(host=api_host, mac=mac)

    ret, err = client.call(path=api_path)
    if err is not None:
        print "Fetch image file\"%s\" failed" % url
        print err
        return None
    else:
        print "Fetch \"%s\" to qiniu \"%s\" success!" % (url,dest_entry)
        return "http://%s.qiniudn.com/%s" % (bucket,quote(filename.encode('utf-8')))
    pass

def akbmember(url,saveto,extra = None):
    start = datetime.datetime.now()
    append = lambda a : 'http://www.akb48.co.jp' + a
    XPATH_DICT = {
        "name"           : "//div[@id='detail_box']/table/tr/td/h3/span[@class='notranslate']",
        "eng_name"       : "//div[@id='detail_box']/table/tr/td/span[@class='furigana_alp']",
        "avatar_src"      : "//div[@id='detail_box']/table/tr/th/img/@src",
        "managercom"     : "//div[@id='detail_box']/table/tr/td/dl/dd[1]",
        "managercom_href": "//div[@id='detail_box']/table/tr/td/dl/dd[1]/a/@href",
        "team"           : "//div[@id='detail_box']/table/tr/td/@class",
        # "nick"           : "//div[@id='detail_box']/table/tr/td/dl/dd[2]",
        # "birthday_str"   : "//div[@id='detail_box']/table/tr/td/dl/dd[3]",
        # "hometown"       : "//div[@id='detail_box']/table/tr/td/dl/dd[4]",
        "info_dt"        : "//div[@id='detail_box']/table/tr/td/dl/dt",
        "info_dd"        : "//div[@id='detail_box']/table/tr/td/dl/dd",
        "concurrent_str" : "//div[@id='detail_box']/table/tr/td/p",
    }
    info = grabInfo(url, XPATH_DICT, append, prefix = 'akb48', saveto = saveto)
    if info:
        for i in xrange(len(info['info_dt'])):
            k = JAP_TO_KEY.get(info['info_dt'][i],None)
            info[k] = info['info_dd'][i]
        info['birthday'] = str2date(info['birthday_str'])
        info['group'] = 'akb48'
        info['team'] = info['team'].split('_')[-1].upper()
        if info['team'] == 'NO':
            info['team'] = u'研究生'
        elif info['team'] == 'OTONA':
            info['team'] = u'大人'
        if info['concurrent_str']:
            m = RE_CONCURRENT.match(info['concurrent_str'])
            if m :
                g = m.groups()
                info['group'] = g[0]
                info['team'] = g[1].replace(' ','')
                info['concurrent_group'] = g[2]
                info['concurrent_team'] = g[3].replace(' ','')

        save(info)

    end = datetime.datetime.now()
    return "Run time: %fs." % (end - start).total_seconds()

def skemember(url,saveto,extra = None):
    start = datetime.datetime.now()
    append = lambda a : a.replace('.','http://www.ske48.co.jp/profile')
    XPATH_DICT = {
        "name"      : "//dl[@class='profile clearfix']/dd/h3[1]",
        "eng_name"  : "//dl[@class='profile clearfix']/dd/h3[@class='en']",
        "avatar_src" : "//dl[@class='profile clearfix']/dt/img/@src",
        "info"      : "//dl[@class='profile clearfix']/dd/ul/li",
        "concurrent_str" : "//dl[@class='profile clearfix']/dd" ,
    }
    info = grabInfo(url, XPATH_DICT, append, prefix = 'ske48', saveto = saveto)
    if info:
        info['group'] = 'ske48'
        info['team'] = extra.replace(u'チーム','')
        for i in info['info']:
            inf = i.split(u'：')
            k = JAP_TO_KEY.get(inf[0],None)
            if k:
                info[k] = inf[1]
            else:
                info["generation"] = inf[0]
        info['birthday'] = str2date(info['birthday_str'])

        if info.has_key('concurrent_group'):
            m = RE_CONCURRENT.match(info['concurrent_group'])
            if m :
                g = m.groups()
                info['group'] = g[0]
                info['team'] = g[1].replace(' ','')
                info['concurrent_group'] = g[2]
                info['concurrent_team'] = g[3].replace(' ','')

        save(info)

    end = datetime.datetime.now()
    return "Run time: %fs." % (end - start).total_seconds()

    pass

def nmbmember(url,saveto,extra = None):
    start = datetime.datetime.now()
    append = lambda a : 'http://www.nmb48.com/member/' + a
    relative = lambda a,b : a + b
    XPATH_DICT = {
        "name"      : "//div[@id='detail-box']/div[@id='detail-data']/h3[1]",
        "eng_name"  : "//div[@id='detail-box']/div[@id='detail-data']/h3[@class='ruby']",
        "avatar_src" : "//div[@id='detail-box']/img[@class='member-photo']/@src",
        "team"      : "//div[@id='detail-box']/div[@id='detail-data']/ul[@id='detail-list']/div[@class='team_seal2']/img[1]/@src",
        "info"      : "//div[@id='detail-box']/div[@id='detail-data']/ul[@id='detail-list']/li",
    }
    info = grabInfo(url, XPATH_DICT, append,relative, prefix = 'nmb48', saveto = saveto)
    if info:
        RE_TEAM = re.compile(r"\.\./\.\./images/member/seal_(\w+)\.jpg")
        info['team'] = RE_TEAM.match(info['team']).groups()[0].upper()
        if info['team'] == u'KENKYUSEI':
            info['team'] = u'研究生'
        else:
            info['team'] = info['team'].replace('TEAM','').replace('2','II')
        info['group'] = 'nmb48'

        if extra:
            m = re.match(r"([A-Za-z]{3}\d{2}) *Team([A-Za-z ]+)[/ \n]*(\w{3}\d{2}) *Team *([A-Za-z ]+)",extra)
            if m:
                g = m.groups()
                info['group'] = g[0]
                info['team'] = g[1].replace(' ','')
                info['concurrent_group'] = g[2]
                info['concurrent_team'] = g[3].replace(' ','')
                pass

        for i in info['info']:
            inf = i.split(':')
            k = JAP_TO_KEY.get(inf[0].strip(),None)
            if k:
                info[k] = inf[1].strip()
            else:
                info["generation"] = inf[0].strip()
        info['birthday'] = str2date(info['birthday_str'])

        save(info)

    end = datetime.datetime.now()
    return "Run time: %fs." % (end - start).total_seconds()
    pass

def hktmember(url,saveto,extra = None):
    start = datetime.datetime.now()
    XPATH_DICT = {
        "name"      : "//div[@class='profile_detail']/p[@class='name_j']",
        "eng_name"  : "//div[@class='profile_detail']/p[@class='name_e']",
        "avatar_src" : "//div[@class='profile_picts']/img/@src",
        "team"      : "//div[@class='profile_detail']/p[@class='team']/img/@src",
        "info_dt"   : "//div[@class='profile_detail']/dl/dt",
        "info_dd"   : "//div[@class='profile_detail']/dl/dd",
        "concurrent_str" : "//div[@class='profile_detail']/p[@class='team_j']" ,
    }
    info = grabInfo(url, XPATH_DICT, prefix = 'hkt48', saveto = saveto)
    if info:
        for i in xrange(len(info['info_dt'])):
            k = JAP_TO_KEY.get(info['info_dt'][i],None)
            info[k] = info['info_dd'][i]
        if info['team']:
            info['team'] = info['team'].split('_')[-1].split('.')[0].replace('team','')
        else:
            info['team'] = u'研究生'
        info['birthday'] = str2date(info['birthday_str'])
        info['group'] = 'hkt48'
        if info['concurrent_str']:
            m = re.match(ur'([A-Za-z]{3}\d{2}) *Team *([A-Za-z ]+)[/ \n]*([A-Za-z]{3}\d{2}) *Team *([A-Za-z ]+) *兼任',info['concurrent_str'])
            if m :
                g = m.groups()
                info['group'] = g[0]
                info['team'] = g[1].replace(' ','')
                info['concurrent_group'] = g[2]
                info['concurrent_team'] = g[3].replace(' ','')

        save(info)

    end = datetime.datetime.now()
    return "Run time: %fs." % (end - start).total_seconds()
    pass


def snhmember(url,saveto):
    pass

def ngzkmember(url,saveto):
    pass


def save(info):
    from crawler.models import OfficialInfo, Relation
    m = OfficialInfo()
    m.name            = info.get('name','')
    m.nick            = info.get('nick','')
    m.eng_name        = info.get('eng_name','')
    m.team            = info.get('team','')
    m.group           = info.get('group','')
    m.concurrent_group= info.get('concurrent_group','')
    m.concurrent_team = info.get('concurrent_team','')
    m.avatar_src      = info.get('avatar_src','')
    m.avatar          = info.get('avatar','')
    m.managercom      = info.get('managercom','')
    m.managercom_href = info.get('managercom_href','')
    m.birthday_str    = info.get('birthday_str','')
    m.birthday        = info.get('birthday',None)
    m.bloodtype       = info.get('bloodtype','')
    m.hometown        = info.get('hometown','')
    m.height          = info.get('height','')
    m.catchphrase     = info.get('catchphrase','')
    m.stunt           = info.get('stunt','')
    m.dream           = info.get('dream','')
    m.favfood         = info.get('favfood','')
    m.favquote        = info.get('favquote','')
    m.msg             = info.get('msg','')
    m.hobby           = info.get('hobby','')
    m.charm           = info.get('charm','')

    r = Relation.objects.get_or_create(jp_name = m.name)[0]
    if r.mid:
        m.mid = r.mid
    m.save()
    pass
