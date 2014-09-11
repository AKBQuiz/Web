# -*- coding:utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from memberinfo.models import MemberInfo,Group,Team
from memberinfo.warpper import warp,member2dic,members2list
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db.models import Q

def APItransform(data,format,rebuilder=None):
    if rebuilder:
        data = rebuilder(data)
    if format == 'json':
        return HttpResponse(warp(data,'json'), mimetype = 'application/json')
    elif format == 'xml':
        return HttpResponse(warp(data,'xml'), mimetype = 'application/xml')
    else:
        raise Http404('Format unavailable')
    pass

def index(request):
    return HttpResponse("123")
    pass

def grouplist(request):
    format = request.GET.get('format',None)
    gl = Group.objects.exclude(groupname__iexact='unknown')
    if format:
        r = lambda x: [{
            'id':g.id,
            'name':g.groupname,
            'founded':g.founded,
            'description':g.description,
            'url':'/database/group_%s/' % g.groupname.lower()
        }for g in x]
        return APItransform(gl,format,r)
    else:
        return render_to_response('grouplist.html', {'groups':gl}, context_instance = RequestContext(request))

def group(request,groupname):
    format = request.GET.get('format',None)
    try:
        g = Group.objects.get(groupname__iexact=groupname)
        if format:
            r = lambda x: {
                'id':x.id,
                'name':x.groupname,
                'founded':x.founded,
                'description':x.description,
                'url':'/database/group_%s/' % x.groupname.lower()
            }
            return APItransform(g,format,r)
        else:
            return render_to_response('groupinfo.html', {'group':g}, context_instance = RequestContext(request))
        pass
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" conflict!' % groupname)

def group_teamlist(request,groupname):
    format = request.GET.get('format',None)
    tl = Team.objects.select_related('group').filter(group__groupname__iexact = groupname).exclude(teamname__iexact='unknown')
    if format:
        r = lambda x: [{
            'id':t.id,
            'name':t.teamname,
            'founded':t.founded,
            'description':t.description,
            'url':'/database/group_%s/team_%s' % (t.group.groupname.lower(), t.teamname.lower())
        }for t in x]
        return APItransform(tl,format,r)
    else:
        return render_to_response('teamlist.html', {'group':groupname,'teams':tl}, context_instance = RequestContext(request))
    pass

def group_memberlist(request,groupname):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(team__group__groupname__iexact = groupname)\
        .exclude(team__teamname__iexact='unknown')\
        .exclude(state__lte=1)
    members = members2list(ml)
    if format:
        return APItransform(ml,format)
    else:
        return render_to_response('memberlist.html', {'title':groupname,'members':members}, context_instance = RequestContext(request))

def group_team(request,groupname,teamname):
    format = request.GET.get('format',None)
    if teamname.lower() in ('ken','kenkyusei'):
        teamname = u"\u7814\u7a76\u751f"
    try:
        t = Team.objects.select_related('group').get(teamname__iexact=teamname,group__groupname__iexact=groupname)
        if format:
            r = lambda x : {
                'id':x.id,
                'name':x.teamname,
                'founded':x.founded,
                'description':x.description,
                'url':'/database/group_%s/team_%s' % (x.group.groupname, x.teamname.lower())
            }
            return APItransform(t,format,r)
        else:
            return render_to_response('teaminfo.html', {'team':t}, context_instance = RequestContext(request))

    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" or Team name "%s" conflict!' % (groupname,teamname))
    pass

def group_team_memberlist(request,groupname,teamname):
    format = request.GET.get('format',None)
    if teamname.lower() in ('ken','kenkyusei'):
        teamname = u"\u7814\u7a76\u751f"
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(team__group__groupname__iexact = groupname,team__teamname__iexact=teamname)\
        .exclude(state__lte=1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response(
            'memberlist.html',
            {'title':groupname + " Team " + teamname,'members':members},
            context_instance = RequestContext(request))

def member(request,mid):
    format = request.GET.get('format',None)
    try:
        m = MemberInfo.objects.select_related('team__group','bothin__group','grade_group').get(mid=mid)
        member = member2dic(m)
        if format:
            return APItransform(member,format)
        else:
            return render_to_response('memberinfo.html', {'member':member}, context_instance = RequestContext(request))
        pass
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : MemberInfo id "%s" conflict!' % mid)

def avatar(request,mid):
    m = get_object_or_404(MemberInfo,mid=mid)
    if not m.avatar is None:
        return HttpResponseRedirect(m.avatar)
    else:
        raise Http404("avatar not founded")


def name(request, name):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group') \
        .filter( Q(cn_name__icontains=name) | Q(name__icontains=name) ).all()
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response(
            'memberlist.html',
            {'title':u'名字中有 "%s" 的'%name,'members':members},
            context_instance = RequestContext(request))
    pass

def birthday_year(request,year):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__year = year).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response(
            'memberlist.html',
            {'title':u'出生年为%s年的' % year,'members':members},
            context_instance = RequestContext(request))

def birthday_date(request,month,day):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__month = month, birthday__day = day).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response(
            'memberlist.html',
            {'title':u'生日为%s月%s日的' % (month,day),'members':members},
            context_instance = RequestContext(request))

def birthday_month(request,month):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__month = month).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response(
            'memberlist.html',
            {'title':u'生日为%s月的' % month,'members':members},
            context_instance = RequestContext(request))

def birthday_day(request,day):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__day = day).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response('memberlist.html',
            {'title':u'生日为%s日的' % day,'members':members},
            context_instance = RequestContext(request))

def birthday_weekday(request,weekday):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__week_day = weekday).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

def birthday(request,year,month,day):
    format = request.GET.get('format',None)
    from datetime import date
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday = date(int(year),int(month),int(day))).exclude(state__lt = 1).all()
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response(
            'memberlist.html',
            {'title':u'生日为%s年%s月%s日的' % (year,month,day),'members':members},
            context_instance = RequestContext(request))

def birthday_range(request,yearfrom,monthfrom,dayfrom,yearto,monthto,dayto):
    format = request.GET.get('format',None)
    from datetime import date
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__range = (
            date(int(yearfrom),int(monthfrom),int(dayfrom)),
            date(int(yearto),int(monthto),int(dayto))
        )).exclude(state__lt = 1).all()
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response('memberlist.html',
            {'title':u'生日为%s年%s月%s日到为%s年%s月%s日之间的' % (yearfrom,monthfrom,dayfrom,yearto,monthto,dayto),'members':members},
            context_instance = RequestContext(request))
    pass


def birthday_span(request,year,month,day,span):
    format = request.GET.get('format',None)
    from datetime import date, timedelta
    datefrom = date(int(year),int(month),int(day))
    dateto = datefrom + timedelta(days=int(span))
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__range = (datefrom, dateto)
        ).exclude(state__lt = 1).all()
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response('memberlist.html',
            {'title':u'生日为%s年%s月%s日开始到之后%s天之间的' % (year,month,day,span),'members':members},
            context_instance = RequestContext(request))
    pass

def birthday_date_range(request,monthfrom,dayfrom,monthto,dayto):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .extra(where=["`birthday` BETWEEN CAST(CONCAT(YEAR(`birthday`), %s) AS DATE) AND CAST(CONCAT(YEAR(`birthday`), %s) AS DATE) "],
            params=['-%s-%s' % (monthfrom, dayfrom), '-%s-%s' % (monthto, dayto)]
         ).exclude(state__lt = 1).all()
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response('memberlist.html',
            {'title':u'生日为%s月%s日到为%s月%s日之间的' % (monthfrom,dayfrom,monthto,dayto),'members':members},
            context_instance = RequestContext(request))
    pass

def birthday_date_span(request,month,day,span):
    format = request.GET.get('format',None)

    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .extra(where=["(`birthday` - CAST(CONCAT(YEAR(`birthday`), %s ) AS DATE)) BETWEEN 0 AND %s "],
            params=['-%s-%s' % (month, day), span]
         ).exclude(state__lt = 1).all()
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response('memberlist.html',
            {'title':u'生日为%s月%s日开始到之后%s天之间的' % (month,day,span), 'members':members},
            context_instance = RequestContext(request))
    pass

def hometown_name(request,divname):
    format = request.GET.get('format',None)
    from memberinfo.divisions import searchIdByEn
    divid = searchIdByEn(divname.lower())
    if divid <= 0:
        raise Http404("request not founded")
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(comefrom = divid).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        return render_to_response('memberlist.html',
            {'title':u'家乡是%s的'%divname,'members':members},
            context_instance = RequestContext(request))

def hometown_id(request,divid):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(comefrom = divid).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        return APItransform(members,format)
    else:
        from memberinfo.divisions import get
        return render_to_response('memberlist.html',
            {'title':u'家乡是%s的'%get(divid),'members':members},
            context_instance = RequestContext(request))

def generation(request,ggroup, gnum):
    format = request.GET.get('format',None)
    try:
        g = Group.objects.get(groupname__iexact=ggroup)
        ml = t.memberinfo_set.select_related('team__group','bothin__group','grade_group')\
            .filter(grade_num__iexact=gnum).exclude(state__lt=1)
        members = members2list(ml)
        if format:
            return APItransform(members,format)
        else:
            return render_to_response('memberlist.html',
                {'title':u'%s %s期的' % (ggroup, gnum),'members':members},
                context_instance = RequestContext(request))
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" conflict!' % groupname)

