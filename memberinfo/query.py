# -*- coding: utf-8 -*-

import datetime

from memberinfo.models import MemberInfo
from django.db.models import Q



def toJson(data):
    import json
    return json.dumps(data,indent=2)

def toXml(data):
    from lxml import etree
    rootarray = etree.Element('array')
    for i in data:
        member = etree.SubElement(rootarray, 'member')
        id_ = etree.SubElement(member, 'id')
        id_.text = unicode(i['id'])
        name = etree.SubElement(member, 'name')
        name.text = i.name
        group = etree.SubElement(member, 'team')
        name.text = i.team.group
        team = etree.SubElement(member, 'team')
        team.text = i.team
        comefrom = etree.SubElement(member, 'comefrom')
        comefrom.text = i.comefrom
        birthday = etree.SubElement(member, 'birthday')
        birthday.text = i.birthday
    pass

def wapper(memberlist, grouping = ''):
    from itertools import groupby
    results = {}
    if grouping == 'team':
        l = lambda i : i.team
        memberlist = sorted(memberlist, key = l)
        return u'\n'.join([u'%s:\n%s'%(k,u'\n'.join([i.name for i in v])) for k,v in groupby(memberlist, key = l)])

    elif grouping == 'birthday':
        l = lambda i : i.birthday.strftime('%B %d')
        memberlist = sorted(memberlist, key = l)
        return u'\n'.join([u'%s:\n%s'%(k,u'\n'.join([u'%s %s %s年' % (i.team, i.name, i.birthday.year) for i in v])) for k,v in groupby(memberlist, key = l)])
    elif grouping == 'birthyear':
        l = lambda i : i.birthday.year
        memberlist = sorted(memberlist, key = l)
        return u'\n'.join([u'%s年:\n%s'%(k,'\n'.join([u'%s %s %s' % (i.team, i.name, i.birthday.strftime('%B %d')) for i in v])) for k,v in groupby(memberlist, key = l)])
    elif grouping == 'birthmonth':
        l = lambda i : i.birthday.month
        memberlist = sorted(memberlist, key = l)
        return u'\n'.join([u'%s月:\n%s'%(k,'\n'.join([u'%s %s %s日' % (i.team, i.name, i.birthday.day) for i in v])) for k,v in groupby(memberlist, key = l)])
    elif grouping == 'birthweekday':
        l = lambda i : i.birthday.strftime('%A')
        memberlist = sorted(memberlist, key = l)
        return u'\n'.join(['%s:\n%s'%(k,'\n'.join(['%s %s' % (i.team, i.name) for i in v])) for k,v in groupby(memberlist, key = l)])
    elif grouping == 'comefrom':
        from memberinfo.divisions import get
        l = lambda i : i.comefrom
        memberlist = sorted(memberlist, key = l)
        return u'\n'.join(['%s:\n%s'%(get(k),'\n'.join(['%s %s' % (i.team, i.name) for i in v])) for k,v in groupby(memberlist, key = l)])
    else:
        return u'\n'.join(['%s %s' % (i.team, i.name) for i in memberlist])
        pass

def byBirthDate(month, date, kenkyu = False, graduated = True):
    memberlist = MemberInfo.objects.filter(
        Q(birthday__month = month) &
        Q(birthday__day = date)
    ).exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist.all()
    return memberlist

def byBirthDateRange(month,date,days, kenkyu = False, graduated = True):
    startdate = datetime.date.today()
    startdate = startdate.replace(month = month, day = date)
    delt = datetime.timedelta(days = days)
    enddate = startdate + delt

    sMon = startdate.month
    sDay = startdate.day
    eMon = enddate.month
    eDay = enddate.day

    memberlist = MemberInfo.objects.extra(
        where = ['MONTH(`birthday`) BETWEEN %s AND %s',
            'NOT (MONTH(`birthday`) = %s AND DAY(`birthday`) < %s)',
            'NOT (MONTH(`birthday`) = %s AND DAY(`birthday`) >= %s)',
        ],
        params = [sMon, eMon, sMon, sDay, eMon, eDay]
    ).exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist.all()
    return memberlist

def byBirthWeekDay(dayinweek, kenkyu = False, graduated = True):
    memberlist = MemberInfo.objects.filter(birthday__week_day =  dayinweek).exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist.all()
    return memberlist

def byBirthMonth(month, kenkyu = False, graduated = True):
    memberlist = MemberInfo.objects.filter(birthday__month = month).exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist.all()
    return memberlist

def byBirthYear(year, kenkyu = False, graduated = True):
    memberlist = MemberInfo.objects.filter(birthday__year = year).exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist.all()
    print memberlist
    return memberlist


def byTeam(teamstr, kenkyu = False, graduated = True):
    teamstr = teamstr.lstrip('team')
    teamstr = teamstr.strip()
    from memberinfo.models import Team
    try:
        teamlist = Team.objects.filter(teamname__icontains = teamstr).exclude(teamname__icontains = 'unknown').all()
    except:
        return 'error: team not found'

    results = [i.memberinfo.all() for i in teamlist]
    memberlist = []
    for i in results:
        memberlist.extend(i)
    memberlist.exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist
    return  memberlist

def byHometown(comefrom, kenkyu = False, graduated = True):
    from memberinfo.divisions import searchIdByCn
    comefrom = comefrom.strip()
    comids = searchIdByCn(comefrom)
    if len(comids) == 0 :
        return 'error: division not found'
        pass
    results = [MemberInfo.objects.filter(comefrom = id_).all() for id_ in comids]
    memberlist = []
    for i in results:
        memberlist.extend(i)
    memberlist.exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist
    return memberlist

def byName(name, kenkyu = False, graduated = True):
    name = name.strip()
    memberlist = MemberInfo.objects.filter(name__icontains = name).exclude(state__lt = 1)
    if not kenkyu:
        memberlist = memberlist.exclude(state = 3)
    if not graduated:
        memberlist = memberlist.exclude(state = 2)
        pass
    memberlist = memberlist.all()
    return memberlist
