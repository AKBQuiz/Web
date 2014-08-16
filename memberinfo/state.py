# -*- coding:utf-8 -*-

from memberinfo.models import MemberInfo, Team
import datetime

for member in MemberInfo.objects.all():
    if not member.graduate == datetime.date.min :
        member.state = 2
        member.save()
        continue

unkonwnteam = Team.objects.filter(teamname__icontains = 'unknown').all()
print unkonwnteam
for team in unkonwnteam:
    for member in team.memberinfo.all():
        member.state = 0
        member.save()
        continue
    pass

kenteam = Team.objects.filter(teamname__icontains = '研究生').all()
print kenteam
for team in kenteam:
    for member in team.memberinfo.all():
        if not member.graduate == datetime.date.min :
            member.state = 0
            member.save()
            continue
        else:
            member.state = 3
            member.save()
        continue
    pass

