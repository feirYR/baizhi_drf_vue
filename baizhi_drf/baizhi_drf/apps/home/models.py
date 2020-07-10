from django.db import models
from home.BaseModel import BaseModel
# Create your models here.
class Banner(BaseModel):
    image=models.ImageField(upload_to='banner',max_length=200,verbose_name='轮播图')
    title=models.CharField(max_length=200,verbose_name='轮播图名称')
    link=models.CharField(max_length=300,verbose_name='轮播图链接')

    class Meta:
        db_table='bz_banner'
        verbose_name='轮播图'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title

class Navigation(BaseModel):
    position_choice=(
        (0,'顶部'),
        (1,'底部'),
    )
    title=models.CharField(max_length=200,verbose_name='导航标题')
    link=models.CharField(max_length=300,verbose_name='导航链接')
    position=models.SmallIntegerField(choices=position_choice,default=0)
    is_site=models.BooleanField(default=False,verbose_name='外部链接')

    class Meta:
        db_table = 'bz_nav'
        verbose_name = '导航'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


