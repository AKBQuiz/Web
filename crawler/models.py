from django.db import models
from memberinfo.models import MemberInfo,Group

class OfficialInfo(models.Model):
    """memberinfo get by crawler"""
    mid             = models.ForeignKey(MemberInfo, blank=True, null=True)
    name            = models.CharField(max_length = 32,)
    nick            = models.CharField(max_length = 32, blank=True,)
    eng_name        = models.CharField(max_length = 32, blank=True,)
    group           = models.CharField(max_length = 8, blank=True,)
    team            = models.CharField(max_length = 8, blank=True,)
    concurrent_group= models.CharField(max_length = 8, blank=True,)
    concurrent_team = models.CharField(max_length = 8, blank=True,)
    avatar_src      = models.URLField(blank=True, null=True,)
    avatar          = models.URLField(blank=True, null=True,)
    managercom      = models.CharField(max_length = 32, blank=True,)
    managercom_href = models.URLField(blank=True, null=True,)
    birthday_str    = models.CharField(max_length = 32, blank=True,)
    birthday        = models.DateField(null = True, blank=True,)
    bloodtype       = models.CharField(max_length = 4, blank=True,)
    hometown        = models.CharField(max_length = 8, blank=True,)
    height          = models.CharField(max_length = 8, blank=True,)
    catchphrase     = models.CharField(max_length = 256, blank=True,)
    stunt           = models.CharField(max_length = 128, blank=True,)
    dream           = models.CharField(max_length = 64, blank=True,)
    favfood         = models.CharField(max_length = 64, blank=True,)
    favquote        = models.CharField(max_length = 64, blank=True,)
    msg             = models.CharField(max_length = 256, blank=True,)
    hobby           = models.CharField(max_length = 128, blank=True,)
    charm           = models.CharField(max_length = 64, blank=True,)
    createdate      = models.DateTimeField(auto_now_add = True, )
    # avatar_fetched  = models.BooleanField(default = False, )
    applied         = models.BooleanField(default = False, )

    def __str__(self):
        return "%s %s (applied: %s)" % (self.name, self.createdate, self.applied)
        pass
    def __unicode__(self):
        return u"%s %s (applied: %s)" % (self.eng_name, self.createdate, self.applied)
        pass

# class Avatar(models.Model):
#     """avatar get by crawler"""
#     mamber       = models.ForeignKey(MemberInfo,null=True)
#     group        = models.ForeignKey(Group)
#     src          = models.URLField(blank=True, null=True,)
#     etag         = models.CharField(max_length = 32, blank=True,)
#     lastmodified = models.DateTimeField(blank=True, null=True,)
#     qiniu_url    = models.URLField(blank=True, null=True,)
#     storage_url  = models.URLField(blank=True, null=True,)

class Relation(models.Model):
    mid          = models.ForeignKey(MemberInfo, blank=True, null=True)
    jp_name      = models.CharField(max_length = 32,)

    def __str__(self):
        return "%s -> %s" % (self.jp_name, self.mid)
        pass
    def __unicode__(self):
        return u"%s -> %s" % (self.jp_name, self.mid)
        pass
