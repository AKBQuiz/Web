from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    """docstring for UserProfile"""
    user = models.OneToOneField(User, unique=True)

    display_name = models.CharField(max_length=32)
    # timezone = models.CharField(max_length=32)
    # lang = models.CharField(max_length=12)
    avatar = models.URLField(blank=True)
    
    weibo_id = models.CharField(max_length=100, blank=True)
    weibo_info = models.TextField(blank=True)

    weixin_id = models.CharField(max_length=100, blank=True)
    weixin_info = models.TextField(blank=True)

    qq_id = models.CharField(max_length=100, blank=True)
    qq_info = models.TextField(blank=True)

    renren_id = models.CharField(max_length=100, blank=True)
    renren_info = models.TextField(blank=True)

    baidu_id = models.CharField(max_length=100, blank=True)
    baidu_info = models.TextField(blank=True)

    #job = models.CharField(max_length=32, blank=True)
    birthday = models.DateField(blank=True, null=True)
    class Meta:
        db_table = u'user_profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance, display_name = instance.username);

post_save.connect(create_user_profile, sender=User)
