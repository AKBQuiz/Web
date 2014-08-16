from __future__ import unicode_literals

from django.db import models

class OldQuizMemberInfo(models.Model):
    field_id = models.IntegerField(db_column='_id', primary_key=True) # Field renamed because it started with '_'.
    name = models.TextField()
    nickname = models.TextField(blank=True)
    group = models.TextField()
    team = models.TextField(blank=True)
    bothin_group = models.TextField(blank=True)
    bothin_team = models.TextField(blank=True)
    grade = models.TextField()
    comefrom = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    graduate = models.DateField(blank=True, null=True)
    was_in = models.TextField(blank=True)
    was_in2 = models.TextField(blank=True)
    is_show = models.BooleanField()

    def __str__(self):
        return "%s, %s Team %s" % (self.name, self.group, self.team)

    class Meta:
        db_table = 'member_info'

class OldQuiz(models.Model):
    field_id = models.IntegerField(db_column='_id', blank=True, primary_key=True) # Field renamed because it started with '_'.
    editor = models.TextField(blank=True)
    question = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    wrong_1 = models.TextField(blank=True)
    wrong_2 = models.TextField(blank=True)
    wrong_3 = models.TextField(blank=True)
    difficulty = models.IntegerField(blank=True, null=True)
    akb48 = models.BooleanField()
    ske48 = models.BooleanField()
    nmb48 = models.BooleanField()
    hkt48 = models.BooleanField()
    sdn48 = models.BooleanField()
    jkt48 = models.BooleanField()
    snh48 = models.BooleanField()
    ngzk46 = models.BooleanField()
    create_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Question : %s,  editor:%s \n answer : %s" % (self.question, self.editor, self.answer)

    class Meta:
        db_table = 'quiz'

class OldQuizCollected(models.Model):
    field_id = models.IntegerField(db_column='_id', blank=True, primary_key=True) # Field renamed because it started with '_'.
    editor = models.TextField(blank=True)
    question = models.TextField(blank=True)
    answer = models.TextField(blank=True)
    wrong_1 = models.TextField(blank=True)
    wrong_2 = models.TextField(blank=True)
    wrong_3 = models.TextField(blank=True)
    difficulty = models.IntegerField(blank=True, null=True)
    akb48 = models.BooleanField()
    ske48 = models.BooleanField()
    nmb48 = models.BooleanField()
    hkt48 = models.BooleanField()
    sdn48 = models.BooleanField()
    jkt48 = models.BooleanField()
    snh48 = models.BooleanField()
    ngzk46 = models.BooleanField()
    create_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Question : %s,  editor:%s \n answer : %s" % (self.question, self.editor, self.answer)

    class Meta:
        db_table = 'quiz_collected'