from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class WxStatus(models.Model):
    user     = models.OneToOneField(User,blank = True, null=True)
    wxOpenID = models.CharField(max_length = 32)
    menuNav  = models.CharField(max_length = 3, default = 'n')
    data     = models.CharField(max_length = 3, default = 'n')
    qSetting = models.CharField(max_length = 16, default = '')
    gSetting = models.CharField(max_length = 16, default = '')
