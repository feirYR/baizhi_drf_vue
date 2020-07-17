from django.db import models
class BaseModel(models.Model):
    is_show=models.BooleanField(default=False,verbose_name='是否显示')
    is_delete=models.BooleanField(default=False,verbose_name='是否删除')
    ordering=models.SmallIntegerField(default=1,verbose_name='排序')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time=models.DateTimeField(auto_now=True,verbose_name='修改时间')
    class Meta:
        abstract = True