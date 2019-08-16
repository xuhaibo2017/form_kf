from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16, verbose_name='用户名')
    password = models.CharField(max_length=16, verbose_name='密码')
    nickname = models.CharField(max_length=16,verbose_name='昵称')
    email = models.EmailField(max_length=20, verbose_name='邮箱')
    #img = models.ImageField(verbose_name='头像',upload_to='static/img/user/',default='static/img/user/1.jpg')
    ctime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name_plural = u'用户管理'