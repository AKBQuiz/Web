# -*- coding: utf-8 -*-
from django.http import HttpResponse,Http404,HttpResponseForbidden
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
import infocrawler as ic

def info(request, group):
    url = request.GET['u']
    save = request.GET.get('s', 'no')
    extra = request.GET.get('e', None)
    res = ic.taskHandler(group, url, save, extra)
    if res:
        return HttpResponse(res)
    else:
        raise Http404

def infostart(request, group):
    if group:
        res = ic.startQueue(group)
        if res:
            return HttpResponse(res)
        else:
            raise Http404
    else:
        return HttpResponse("This is a crawler.")

def infoapply(request):
    ultra = False
    from crawler.models import OfficialInfo,Relation
    from memberinfo.models import MemberInfo,Group,Team
    import memberinfo.divisions as div

    if request.GET.has_key('ultra'):
        if not request.user.is_staff:
            return HttpResponseForbidden('You are not a staff of this site.')
        else:
            ultra = True
            rela = Relation.objects.filter(mid__isnull = False)
            for r in rela:
                OfficialInfo.objects.filter(mid__isnull = True, name__iexact = r.jp_name).update(mid = r.mid)
            pass
    counter = 0
    infolist = OfficialInfo.objects.filter(mid__isnull = False, applied = False).all()
    namelist = infolist.values('name').all()
    for name in namelist:
        items = infolist.filter(name__iexact = name['name']).all()
        member = {}
        for item in items:
            for k in item._meta.get_all_field_names():
                v = getattr(item,k)
                if v:
                    member[k] = v
        try:
            m = member['mid']
            g = Group.objects.get(groupname__iexact = member['group'])
            t = g.team_set.get(teamname__iexact = member['team'])
            m.team = t
            m.comefrom = div.getIdByJp(member['hometown'])
            m.birthday = member['birthday']
            if ultra:
                from memberinfo.cn_jp import jp2cn
                m.name = member['name']
                l = []
                for c in m.cn_name:
                    l.append(jp2cn(c))
                m.cn_name = ''.join(l)

            if member.get('nick', False):
                m.nick = member['nick']
            if member.get('avatar', False):
                m.avatar = member['avatar']
            if member.get('concurrent_group',False):
                cg = Group.objects.get(groupname__iexact = member['concurrent_group'])
                ct = cg.team_set.get(teamname__iexact = member['concurrent_team'])
                m.bothin = ct
                pass

            des = []
            if member.get('managercom',False):
                if member.get('managercom_href',False):
                    des.append(u'经纪公司：<a href="' + member['managercom_href'] + '">' + member['managercom'] + '</a>')
                else:
                    des.append(u'经纪公司：' + member['managercom'])
            if member.get('bloodtype',False):
                des.append(u'血型：' + member['bloodtype'])
            if member.get('height',False):
                des.append(u'身高：' + member['height'])
            if member.get('catchphrase',False):
                des.append(u'Catch Phrase：' + member['catchphrase'])
            if member.get('stunt',False):
                des.append(u'特技：' + member['stunt'])
            if member.get('dream',False):
                des.append(u'梦想：' + member['dream'])
            if member.get('favfood',False):
                des.append(u'最爱的食物：' + member['favfood'])
            if member.get('favquote',False):
                des.append(u'座右铭：' + member['favquote'])
            if member.get('favfood',False):
                des.append(u'最爱的食物：' + member['favfood'])
            if member.get('hobby',False):
                des.append(u'爱好：' + member['hobby'])
            if member.get('charm',False):
                des.append(u'魅力点：' + member['charm'])
            if member.get('msg',False):
                des.append(member['msg'])
            m.description = '<br />'.join(des)
            m.save()
            counter += 1
        except Exception, e:
            print e
            continue
        items.update(applied = True)
        pass
    return HttpResponse('info of %d members applied.' % counter)
    pass

def autorelation(request):
    from crawler.models import Relation,OfficialInfo
    from memberinfo.models import MemberInfo
    rela = Relation.objects.filter(mid__isnull = True)
    counter = 0
    for r in rela:
        try:
            m = MemberInfo.objects.get(name__iexact = r.jp_name)
            r.mid = m
            r.save()
            counter += OfficialInfo.objects.filter(mid__isnull = True, name__iexact = r.jp_name).update(mid = m)
        except Exception as e:
            print e
            continue
    return HttpResponse("%d relations auto solved." % counter)
    pass

@login_required
def relation(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('You are not a staff of this site.')
    if request.method == 'POST':
        counter = 0
        for k in request.POST:
            rid = int(k[4:])
            mid = int(request.POST[k])
            from crawler.models import Relation,OfficialInfo
            from memberinfo.models import MemberInfo
            if mid < 0:
                continue
            try:
                r = Relation.objects.get(id=rid)
                if mid > 0 :
                    m = MemberInfo.objects.get(mid=mid)
                elif mid == 0 :
                    m = MemberInfo.objects.create(name = r.jp_name)
                r.mid = m
                OfficialInfo.objects.filter(mid__isnull = True, name__iexact = r.jp_name).update(mid = m)
                r.save()
                counter += 1
                pass
            except Exception, e:
                print e
            pass
        return HttpResponse("{\"state\":\"success\",\"num\": %d }" % counter)
    elif request.method == 'GET':
        return render_to_response("relation.html", context_instance = RequestContext(request))
    else:
        raise Http404

def relationunsolved(request,start,end):
    if request.method == 'GET':
        import json
        from crawler.models import Relation
        from memberinfo.models import Team
        rela = Relation.objects.filter(mid__isnull = True)[start:end]
        return HttpResponse(json.dumps([{"rid":r.id,"name":r.jp_name} for r in rela]))
    pass

def schedule(request):
    pass

def index(request):
    return HttpResponse("This is a crawler.")
    pass


