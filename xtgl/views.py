from django.shortcuts import render
import pymysql
import time
import sys,os
from django.core.paginator import Paginator
from .models import MAC_IP

# Create your views here.
def aqzm(req,time1=None):
    """"""
    """初始化数据库连接，游标，数据库表名"""
    if time1 is None:
        time1=time.strftime('%Y%m%d',time.localtime(time.time()))
    time2=time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
    db=pymysql.connect(host="66.3.59.102",user="aqzm",passwd="123456",db="aqzm",port=3306,charset="utf8")
    cursor=db.cursor()
    #table_name=time.strftime('%Y%m%d',time.localtime(time.time()))+'_count'
    table_name=time1+'_count'
    #table_name2=time.strftime('%Y%m%d',time.localtime(time.time()))+'_detail'
    table_name2=time1+'_detail'
    """查询表并转换成字典"""
    cursor.execute("select * from %s" %table_name)
    rs1=cursor.fetchall()
    count=0
    dict_fu={}
    for key in rs1:
        for j in key:
            count+=1
            if (count % 2)==1:
                key=j
            if (count % 2 )==0:
                dict_fu[key]=j
    """查询表并转换成字典"""
    cursor.execute("select company,count(company) as a  from %s where conn_state='connected' group by company" %table_name2)
    rs2=cursor.fetchall()
    count1=0
    dict_co={}
    for key in rs2:
        for j in key:
            count1+=1
            if (count1 % 2)==1:
                ckey=j
            if (count1 % 2 )==0:
                dict_co[ckey]=j
    dict_con={}
    for key in dict_fu:
        if key in dict_co:
            dict_con[key]=dict_co[key]
        else:
            dict_con[key]=0
    """两个字典数据合并保存到列表"""
    list_a=[]
    list_b=[]
    list_c=[]
    count=0
    for key in dict_fu:
        list_a.append(key)
        list_b.append(dict_fu[key])
        list_c.append(dict_con[key])
    cursor.execute("select user from %s where conn_state='connected'" %table_name2)
    rs_con=cursor.fetchall()
    """查询数据表并将结果写到字典"""
    dict_user={}
    for com in dict_fu:
        cursor.execute("select user from %s where company = '%s' and conn_state='connected'" %(table_name2,com))
        re=cursor.fetchall()
        dict_user[com]=str(re)
    dict_user2={}
    for com in dict_fu:
        cursor.execute("select user from %s where company = '%s' and conn_state='dis_connected'" %(table_name2,com))
        re=cursor.fetchall()
        dict_user2[com]=str(re)

    cpu=20
    memory=80
    dict={'as':1,'bwf':2,'count':3}
    cursor.execute("select count(*) from %s " %table_name2)
    re=cursor.fetchall()
    sum_num=re[0][0]
    cursor.execute("select count(*) from %s where conn_state='connected'" %table_name2)
    re=cursor.fetchall()
    conn_num=re[0][0]
    return render(req,'aqzm_test.html',{'time2':time2,'sum_num':sum_num,'conn_num':conn_num,'cpu':cpu,'memory':memory,"time1":time1,'info_dict':dict_user,'dict_con':dict_con,'dict_fu':dict_fu,'info_dict2':dict_user2,'list2':list_a,'list3':list_b,'list_c':list_c,'user_con':rs_con })
def aqzm_index(req):
    """"""
    """初始化数据库连接，游标，数据库表名"""
    time1=time.strftime('%Y%m%d',time.localtime(time.time()))
    time2=time.strftime('%Y%m%d-%H%M%S',time.localtime(time.time()))
    db=pymysql.connect(host="66.3.59.102",user="aqzm",passwd="123456",db="aqzm",port=3306,charset="utf8")
    cursor=db.cursor()
    table_name=time1+'_count'
    table_name2=time1+'_detail'
    cursor.execute("select table_name from information_schema.tables where table_schema='aqzm'  and table_name like '%_detail';")
    rs1=cursor.fetchall()
    date_list=[]
    for line in rs1:
        date_list.append(line[0].strip('_detail'))

    cursor.execute("select count(*) from %s " %table_name2)
    re=cursor.fetchall()
    sum_num=re[0][0]
    cursor.execute("select count(*) from %s where conn_state='connected'" %table_name2)
    re=cursor.fetchall()
    conn_num=re[0][0]
    return render(req,'aqzm_index.html',{'date_list':date_list,'time1':time1,'sum_num':sum_num,'conn_num':conn_num})

def mac_list(request):
    """
    List all Hosts
    """
    user = request.user
    if request.method =='POST':
        action = request.get_full_path().split('=')[1]
    else:
        mac_list = MAC_IP.objects.all().order_by('-ip_addr')
    paginator = Paginator(mac_list,20)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        mac_list = paginator.page(page)
    except :
        all_mac = paginator.page(paginator.num_pages)

    return render(request, 'mac_ip_list.html', {'mac_list': mac_list, 'page': page, 'paginator':paginator,"username":request.user,})
    # return render(request, 'host_list.html',{'host_list': host_list})