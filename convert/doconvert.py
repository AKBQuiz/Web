from convert.models import *
from quiz.models import *
from memberinfo.models import Group, Team, MemberInfo
from memberinfo.divisions import Division
import datetime 


akb = Group.objects.get(groupname='AKB48');
ske = Group.objects.get(groupname='SKE48');
nmb = Group.objects.get(groupname='NMB48');
hkt = Group.objects.get(groupname='HKT48');
ngzk = Group.objects.get(groupname='NGZK46');
sdn = Group.objects.get(groupname='SDN48');
jkt = Group.objects.get(groupname='JKT48');
snh = Group.objects.get(groupname='SNH48');
u = Group.objects.get(groupname='Unknown');

if akb and ske and nmb and hkt and ngzk and sdn and jkt and snh and u:
    print "Groups Loading Ready"

nullteam = Team.objects.get(teamname = 'Unknown', group__groupname = 'Unknown')

oldQuizList = OldQuiz.objects.using('old').all()
for oldquiz in oldQuizList:
    quiz = Quiz.objects.create(difficulty = 0, state = 1)
    quiz.author_text = oldquiz.editor
    quiz.question = oldquiz.question 
    quiz.answer   = oldquiz.answer   
    quiz.wrong_1  = oldquiz.wrong_1  
    quiz.wrong_2  = oldquiz.wrong_2
    quiz.wrong_3  = oldquiz.wrong_3

    if oldquiz.create_date:
        quiz.createtime = oldquiz.create_date
        pass
     

    if oldquiz.akb48:
        quiz.correlation.add(akb)
        pass
    if oldquiz.ske48:
        quiz.correlation.add(ske)
        pass
    if oldquiz.nmb48:
        quiz.correlation.add(nmb)
        pass
    if oldquiz.hkt48:
        quiz.correlation.add(hkt)
        pass
    if oldquiz.ngzk46:
        quiz.correlation.add(ngzk)
        pass
    if oldquiz.sdn48:
        quiz.correlation.add(sdn)
        pass
    if oldquiz.jkt48:
        quiz.correlation.add(jkt)
        pass
    if oldquiz.snh48:
        quiz.correlation.add(snh)
        pass

    quiz.save() 

oldcollectedList = OldQuizCollected.objects.using('old').all()
for oldcollected in oldcollectedList:
    quiz = Quiz.objects.create(difficulty = 0, state = 0)
    quiz.author_text = oldcollected.editor
    quiz.question = oldcollected.question 
    quiz.answer   = oldcollected.answer   
    quiz.wrong_1  = oldcollected.wrong_1  
    quiz.wrong_2  = oldcollected.wrong_2
    quiz.wrong_3  = oldcollected.wrong_3

    if oldcollected.create_date:
        quiz.createtime = oldcollected.create_date
        pass

    if oldcollected.akb48:
        quiz.correlation.add(akb)
        pass
    if oldcollected.ske48:
        quiz.correlation.add(ske)
        pass
    if oldcollected.nmb48:
        quiz.correlation.add(nmb)
        pass
    if oldcollected.hkt48:
        quiz.correlation.add(hkt)
        pass
    if oldcollected.ngzk46:
        quiz.correlation.add(ngzk)
        pass
    if oldcollected.sdn48:
        quiz.correlation.add(sdn)
        pass
    if oldcollected.jkt48:
        quiz.correlation.add(jkt)
        pass
    if oldcollected.snh48:
        quiz.correlation.add(snh)
        pass

    quiz.save()

oldMemberInfo = OldQuizMemberInfo.objects.using('old').all()
for oldinfo in oldMemberInfo:
    info = MemberInfo.objects.create(
        team = nullteam, 
        grade_group = u,
        state = 1,
        comefrom = 0)

    if oldinfo.group:
        g = Group.objects.get(groupname = oldinfo.group) 
    else:
        g = u;
        pass

    if oldinfo.team:
        info.team = Team.objects.get(teamname__contains = oldinfo.team,group = g)
    else:
        info.team = Team.objects.get(teamname__contains = 'Unknown',group = g)

    info.name        = oldinfo.name
    info.grade_group = Group.objects.get(groupname = oldinfo.grade[:5])
    info.grade_num   = oldinfo.grade[6:]
    info.comefrom    = Division().get('cn',oldinfo.comefrom,'id')
    if oldinfo.birthday and oldinfo.birthday > datetime.date(1980,1,1):
        info.birthday = oldinfo.birthday
        pass
    if oldinfo.graduate and oldinfo.graduate > datetime.date(1980,1,1):
        info.graduate = oldinfo.graduate
        pass

    if oldinfo.nickname:
        info.description = oldinfo.nickname

    if oldinfo.bothin_group:
        g = Group.objects.get(groupname = oldinfo.bothin_group)
        info.bothin = Team.objects.get(teamname__contains = oldinfo.bothin_team, group = g)
        pass

    if not oldinfo.is_show:
        info.state = 0
    info.save()
