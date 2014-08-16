from django.db import models
from django.contrib.auth.models import User
from memberinfo.models import Group

class Quiz(models.Model):
    """docstring for Quiz"""
    author      = models.ForeignKey(User,blank = True, null=True)
    author_text = models.CharField(max_length = 32)

    question    = models.CharField(max_length = 200)
    answer      = models.CharField(max_length = 50)
    wrong_1     = models.CharField(max_length = 50)
    wrong_2     = models.CharField(max_length = 50)
    wrong_3     = models.CharField(max_length = 50)

    difficulty  = models.IntegerField(blank = True)
    correlation = models.ManyToManyField(Group)

    createtime  = models.DateTimeField(auto_now_add = True)
    edittime    = models.DateTimeField(auto_now = True)
    state       = models.IntegerField(choices = ((-1,"deleted"),(0,"received"),(1,"accepted")))

    class Meta:
        db_table = u'quizlist'

class QuizComment(models.Model):
    quiz        = models.ForeignKey(Quiz)
    difficulty  = models.IntegerField(blank = True)
    duplicate   = models.BooleanField(blank = True)
    incorrect   = models.BooleanField(blank = True)
    incoherent  = models.BooleanField(blank = True)
    type_err    = models.BooleanField(blank = True)
    commemt     = models.TextField(blank = True)

    createtime  = models.DateTimeField(auto_now_add = True)
    state       = models.IntegerField(choices = ((-1,"deleted"),(0,"received"),(1,"fixed")))

    class Meta:
        db_table = u'quizcomment'
