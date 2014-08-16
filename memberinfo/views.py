from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from memberinfo.models import MemberInfo,Group,Team
from memberinfo.warpper import warp,member2dic,members2list
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.db.models import Q


def index(request):
    pass

def grouplist(request):
    format = request.GET.get('format',None)
    gl = Group.objects.exclude(groupname__iexact='unknown')
    if format:
        groups = [{'id':g.id,'name':g.groupname, 'founded':g.founded, 'description':g.description, 'url':'/database/group_%s/' % g.groupname.lower() }for g in gl]
        if request.GET['format'] == 'json':
            return HttpResponse(warp(groups,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(groups,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('grouplist.html', {'groups':gl}, context_instance = RequestContext(request))

def group(request,groupname):
    format = request.GET.get('format',None)
    try:
        g = Group.objects.get(groupname__iexact=groupname)
        if format:
            group = {'id':g.id,'name':g.groupname, 'founded':g.founded, 'description':g.description, 'url':'/database/group_%s/' % g.groupname.lower()}
            if request.GET['format'] == 'json':
                return HttpResponse(warp(group,'json'), mimetype = 'application/json')
            elif request.GET['format'] == 'xml':
                return HttpResponse(warp(group,'xml'), mimetype = 'application/xml')
        else:
            return render_to_response('groupinfo.html', {'group':g}, context_instance = RequestContext(request))
        pass
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" conflict!' % groupname)

def group_teamlist(request,groupname):
    format = request.GET.get('format',None)
    try:
        g = Group.objects.get(groupname__iexact=groupname)
        tl = g.team_set.select_related('group').exclude(teamname__iexact='unknown')
        if format:
            teams = [{
                'id':t.id,
                'name':t.teamname,
                'founded':t.founded,
                'description':t.description,
                'url':'/database/group_%s/team_%s' % (t.group.groupname.lower(), t.teamname.lower())
            }for t in tl]
            if request.GET['format'] == 'json':
                return HttpResponse(warp(teams,'json'), mimetype = 'application/json')
            elif request.GET['format'] == 'xml':
                return HttpResponse(warp(teams,'xml'), mimetype = 'application/xml')
        else:
            return render_to_response('teamlist.html', {'group':g,'teams':tl}, context_instance = RequestContext(request))
        pass
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" conflict!' % groupname)

def group_memberlist(request,groupname):
    format = request.GET.get('format',None)
    try:
        g = Group.objects.get(groupname__iexact=groupname)
        tl = g.team_set.exclude(teamname__iexact='unknown')
        q = Q(team = tl[0])
        for t in tl[1:]:
            q = q | Q(team = t)
        ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group').filter( q ).exclude(state__lte=1)
        members = members2list(ml)
        if format:
            if request.GET['format'] == 'json':
                return HttpResponse(warp(members,'json'), mimetype = 'application/json')
            elif request.GET['format'] == 'xml':
                return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
        else:
            return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" conflict!' % groupname)

def group_team(request,groupname,teamname):
    format = request.GET.get('format',None)
    if teamname.lower() in ('ken','kenkyusei'):
        teamname = u"\u7814\u7a76\u751f"
    try:
        g = Group.objects.get(groupname__iexact=groupname)
        t = g.team_set.get(teamname__iexact=teamname)
        if format:
            team = {'id':g.id,'name':t.teamname, 'founded':t.founded, 'description':t.description, 'url':'/database/group_%s/team_%s' % (t.group.groupname,t.teamname.lower())}
            if request.GET['format'] == 'json':
                return HttpResponse(warp(team,'json'), mimetype = 'application/json')
            elif request.GET['format'] == 'xml':
                return HttpResponse(warp(team,'xml'), mimetype = 'application/xml')
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
    try:
        g = Group.objects.get(groupname__iexact=groupname)
        t = g.team_set.get(teamname__iexact=teamname)
        ml = t.memberinfo.select_related('team__group','bothin__group','grade_group').exclude(state__lte=1)
        members = members2list(ml)
        if format:
            if request.GET['format'] == 'json':
                return HttpResponse(warp(members,'json'), mimetype = 'application/json')
            elif request.GET['format'] == 'xml':
                return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
        else:
            return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" or Team name "%s" conflict!' % (groupname,teamname))

def member(request,mid):
    format = request.GET.get('format',None)
    try:
        m = MemberInfo.objects.select_related('team__group','bothin__group','grade_group').get(mid=mid)
        member = member2dic(m)
        if format:
            if request.GET['format'] == 'json':
                return HttpResponse(warp(member,'json'), mimetype = 'application/json')
            elif request.GET['format'] == 'xml':
                return HttpResponse(warp(member,'xml'), mimetype = 'application/xml')
        else:
            return render_to_response('memberinfo.html', {'member':member}, context_instance = RequestContext(request))
        pass
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : MemberInfo id "%s" conflict!' % mid)

def avatar(request,mid):
    try:
        m = MemberInfo.objects.get(mid=mid)
        if not m.avatar is None:
            return HttpResponseRedirect(m.avatar)
        else:
            raise Http404("request not founded")
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : MemberInfo id "%s" conflict!' % mid)

def name(request, name):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group') \
        .filter( Q(cn_name__icontains=name) | Q(name__icontains=name) ).all()
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))
    return HttpResponse(name)
    pass

def birthday_year(request,year):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__year = year).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

def birthday_date(request,month,day):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__month = month, birthday__day = day).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

def birthday_month(request,month):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__month = month).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

def birthday_day(request,day):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__day = day).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

def birthday_weekday(request,weekday):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday__week_day = weekday).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

def birthday(request,year,month,day):
    format = request.GET.get('format',None)
    from datetime import date
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(birthday = date(int(year),int(month),int(day))).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

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
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))

def hometown_id(request,divid):
    format = request.GET.get('format',None)
    ml = MemberInfo.objects.select_related('team__group','bothin__group','grade_group')\
        .filter(comefrom = divid).exclude(state__lt = 1)
    members = members2list(ml)
    if format:
        if request.GET['format'] == 'json':
            return HttpResponse(warp(members,'json'), mimetype = 'application/json')
        elif request.GET['format'] == 'xml':
            return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
    else:
        return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))


def generation(request,ggroup, gnum):
    format = request.GET.get('format',None)
    try:
        g = Group.objects.get(groupname__iexact=ggroup)
        ml = g.memberinfo_set.select_related('team__group','bothin__group','grade_group')\
            .filter(grade_num__iexact=gnum).exclude(state__lt=1)
        members = members2list(ml)
        if format:
            if request.GET['format'] == 'json':
                return HttpResponse(warp(members,'json'), mimetype = 'application/json')
            elif request.GET['format'] == 'xml':
                return HttpResponse(warp(members,'xml'), mimetype = 'application/xml')
        else:
            return render_to_response('memberlist.html', {'members':members}, context_instance = RequestContext(request))
    except ObjectDoesNotExist:
        raise Http404("request not founded")
    except MultipleObjectsReturned:
        return HttpResponse('Error : Group name "%s" conflict!' % groupname)

