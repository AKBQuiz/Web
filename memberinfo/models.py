from django.db import models
from django.contrib.auth.models import User

comfrom_choices = (
        (0,"Unknown"),
        (1,"Hokkaido"),
        (2,"Aomori",),
        (3,"Iwate",),
        (4,"Miyagi",),
        (5,"Akita",),
        (6,"Yamagata",),
        (7,"Fukushima",),
        (8,"Ibaraki",),
        (9,"Tochigi",),
        (10,"Gunma",),
        (11,"Saitama",),
        (12,"Chiba",),
        (13,"Tokyo",),
        (14,"Kanagawa",),
        (15,"Niigata",),
        (16,"Toyama",),
        (17,"Ishikawa",),
        (18,"Fukui",),
        (19,"Yamanashi",),
        (20,"Nagano",),
        (21,"Gifu",),
        (22,"Shizuoka",),
        (23,"Aichi",),
        (24,"Mie",),
        (25,"Shiga",),
        (26,"Kyoto",),
        (27,"Osaka",),
        (28,"Hyogo",),
        (29,"Nara",),
        (30,"Wakayama",),
        (31,"Tottori",),
        (32,"Shimane",),
        (33,"Okayama",),
        (34,"Hiroshima",),
        (35,"Yamaguchi",),
        (36,"Tokushima",),
        (37,"Kagawa",),
        (38,"Ehime",),
        (39,"Kochi",),
        (40,"Fukuoka",),
        (41,"Saga",),
        (42,"Nagasaki",),
        (43,"Kumamoto",),
        (44,"Oita",),
        (45,"Miyazaki",),
        (46,"Kagoshima",),
        (47,"Okinawa",),
    )

class Group(models.Model):
    """docstring for Group"""
    groupname   = models.CharField(max_length = 8)
    founded     = models.DateField()
    description = models.TextField(blank=True)

    createtime  = models.DateTimeField(auto_now_add = True)
    edittime    = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return u"%s" % (self.groupname)

    def __str__(self):
        return "%s" % (self.groupname)

class Team(models.Model):
    """docstring for Team"""

    group       = models.ForeignKey(Group)

    teamname    = models.CharField(max_length = 8)
    founded     = models.DateField()
    description = models.TextField(blank=True)

    createtime  = models.DateTimeField(auto_now_add = True)
    edittime    = models.DateTimeField(auto_now = True)

    # def fullteamname(self):
    #     return u'%s Team %s' % (self.group, self.teamname)
    #     pass

    def __unicode__(self):
        return unicode(self.group.groupname + " Team " +self.teamname)



class MemberInfo(models.Model):
    """docstring for MemberInfo"""
    import datetime

    mid         = models.AutoField(primary_key=True)

    team        = models.ForeignKey(Team, related_name = "memberinfo", null=True,)
    name        = models.CharField(max_length = 32)
    cn_name     = models.CharField(max_length = 32)
    nick        = models.CharField(max_length = 32, blank=True)
    avatar      = models.URLField(blank=True, null = True,)
    grade_group = models.ForeignKey(Group, null = True,)
    grade_num   = models.CharField(max_length = 4,)
    comefrom    = models.IntegerField(choices = comfrom_choices, default = 0)
    birthday    = models.DateField(null=True,)
    graduate    = models.DateField(blank=True, null=True)

    description = models.TextField(blank=True)

    bothin      = models.ForeignKey(Team, related_name = "bothin", blank = True, null = True)

    createtime  = models.DateTimeField(auto_now_add=True)
    edittime    = models.DateTimeField(auto_now=True)

    state       = models.IntegerField(default = 0, choices=((-1,"deleted"),(0,"data accepted"),(1,"graduated"),(2,"kenkyusei"),(3,"regular")))

    def __unicode__(self):
        return u"%s %s" % (self.name, self.team)

    def __str__(self):
        return "%s %s" % (self.name, self.team)


class MemberInfoEdition(models.Model):

    mid         = models.ForeignKey(MemberInfo, null=True)
    uid         = models.ForeignKey(User, null=True)

    team        = models.ForeignKey(Team)
    name        = models.CharField(max_length = 32,blank = True)
    grade_group = models.ForeignKey(Group)
    grade_num   = models.CharField(max_length = 4)
    comefrom    = models.IntegerField(choices = comfrom_choices,blank = True)
    birthday    = models.DateField(blank = True)
    graduate    = models.DateField(blank = True)

    createtime  = models.DateTimeField(auto_now_add=True)
    state       = models.IntegerField(choices=((-1,"rejected"),(0,"normal"),(1,"acceped")))

    def __unicode__(self):
        return u"%s %s (%s)" % (self.name, self.team, self.state)

    def __str__(self):
        return "%s %s (%s)" % (self.name, self.team, self.state)


class Events(models.Model):

    mid         = models.ManyToManyField(MemberInfo)
    uid         = models.ForeignKey(User)

    name        = models.CharField(max_length = 32)
    etype       = models.IntegerField(choices=((0,"move"),(1,"reset"),(2,"bothin"),(3,"finishbothin")))

    datafrom    = models.ForeignKey(Team, related_name = "from")
    datato      = models.ForeignKey(Team, related_name = "to")

    date        = models.DateField()
    description = models.TextField(blank=True)
    state       = models.IntegerField(choices=((-1,"closed"),(0,"acceped"),(1,"normal")))

    createtime  = models.DateTimeField(auto_now_add = True)
    edittime    = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return u"%s %s (%s)" % (self.name, self.etype, self.state)

    def __str__(self):
        return "%s %s (%s)" % (self.name, self.etype, self.state)
