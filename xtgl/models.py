from django.db import models

# Create your models here.
class MAC_IP(models.Model):
    username = models.CharField(max_length=20, verbose_name=u'姓名')
    team = models.CharField(max_length=30, verbose_name=u'所属团队')
    outsourcing_company = models.CharField(max_length=30, verbose_name=u'外部公司')
    floor = models.CharField(max_length=20, verbose_name=u'楼层')
    room_num = models.CharField(max_length=20, verbose_name=u'房间号')
    machine_type = models.CharField(max_length=50, blank=True, verbose_name=u'设备类型')
    machine_num = models.CharField(max_length=50, blank=True, verbose_name=u'设备编号')
    interface = models.CharField(max_length=10, verbose_name=u'网口号')
    mac_addr = models.CharField(max_length=30, verbose_name=u'MAC地址',unique=True)
    ip_addr = models.CharField(max_length=20, verbose_name=u'IP地址',unique=True)
    remark = models.TextField(max_length=250, blank=True, verbose_name=u'备注')
    state = models.CharField(max_length=10, blank=True, verbose_name=u'状态')
    left_time = models.CharField(max_length=30, verbose_name=u'到期时间')
    def __unicode__(self):
        return u'%s - %s - %s' %(self.username, self.ip_addr, self.mac_addr )

    class Meta:
        # verbose_name = u'主机列表'
        verbose_name_plural = u'MAC地址分配列表'