from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserInfo(AbstractUser):
    phone=models.CharField(max_length=11,unique=True,verbose_name='用户手机号')
    photo=models.ImageField(upload_to='user',max_length=200,null=True)

    class Meta:
        db_table='bz_user'
        verbose_name='用户表'
        verbose_name_plural=verbose_name

