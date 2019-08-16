# Generated by Django 2.0 on 2019-08-15 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HostList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20, verbose_name='IP地址')),
                ('hostname', models.CharField(max_length=30, verbose_name='主机名')),
                ('product', models.CharField(max_length=20, verbose_name='产品')),
                ('application', models.CharField(max_length=20, verbose_name='应用')),
                ('idc_jg', models.CharField(blank=True, max_length=10, verbose_name='机柜编号')),
                ('status', models.CharField(default='待装机', max_length=10, verbose_name='使用状态')),
                ('remark', models.TextField(blank=True, max_length=50, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '主机列表管理',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audit_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('type', models.CharField(max_length=20, verbose_name='类型')),
                ('action', models.CharField(max_length=20, verbose_name='动作')),
                ('action_ip', models.CharField(max_length=20, verbose_name='执行IP')),
                ('content', models.CharField(max_length=200, verbose_name='内容')),
            ],
            options={
                'verbose_name_plural': '审计信息管理',
            },
        ),
    ]
