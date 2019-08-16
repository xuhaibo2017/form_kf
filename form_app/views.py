#coding:utf-8
# Create your views here.
from django.shortcuts import render,render_to_response,redirect,HttpResponse,get_object_or_404
from django.core.paginator import Paginator
from io import BytesIO
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from form_app.models import User
from form_test.mysql import db_operate
from form_test import settings
import time
import datetime
from form_app.forms import  UserListForm
from django.urls import  reverse
from asset.models import  Message
from form_test.mysql import db_operate
from form_app.forms import RegisterForm,loginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login  as auth_login,logout as auth_logout
from django.contrib.auth.models import User as User_auth
import json
import pymysql

#表单
'''class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密__码',widget=forms.PasswordInput())
'''
def register(request):
    # username = models.CharField(max_length=16, verbose_name='用户名')
    # password = models.CharField(max_length=16, verbose_name='密码')
    # nickname = models.CharField(max_length=16,verbose_name='昵称')
    # email = models.EmailField(max_length=16, verbose_name='邮箱')
    # img = models.ImageField(verbose_name='头像',upload_to='static/img/user/',default='static/img/user/1.jpg')
    # ctime = models.DateTimeField(auto_created=True,verbose_name='创建时间')

    if request.method == 'GET':
        obj = RegisterForm()
        # return render(request,'register.html',{'form':obj})
    elif request.method == 'POST':
        # print(request.POST)
        obj = RegisterForm(request.POST)
        #post_check_code =  request.POST.get('check_code')
        #session_check_code = request.session['check_code']
        #print(post_check_code,session_check_code)
        if obj.is_valid():
            #if post_check_code ==  session_check_code:
            # values = obj.clean()
                data = obj.cleaned_data
                print(data)
                # models.User.objects.create(
                username= data.get('username')
                password= data.get('pwd')
                email= data.get('email')
                nickname = data.get('username')
                # )
                User.objects.create(username=username,nickname =nickname,password =password,email = email )
                User_auth.objects.create_user(username=username,email=email,password=password)
                #request.session['is_login'] = 'true'
                #request.session['user'] = data.get('username')
                return redirect('/login/')
        #else:
        #    errors = obj.errors
        #    print('hello')
    return render(request,'register.html',{'form':obj})
def login(request):
    if request.method == 'GET':
        obj = loginForm()
        return render(request,'login.html',{'form':obj})
    elif request.method == 'POST':
        obj = loginForm(request.POST)
        errors = {}
        if obj.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('pwd', '')
            user = authenticate(request, username=username, password=password)
            data = obj.cleaned_data
            if user is not None:
                auth_login(request, user)
            #if request.POST.get('auto_login'):
                #request.session.set_expiry(60 * 60 * 24 *30)
            #request.session['is_login'] = 'true'
            #request.session['user'] = data.get('username')
                return render(request,'index_home.html',{'username':request.user})
        return render(request,'login.html',{'form':obj})

@login_required()
def test(request):
    #if req.user.is_anonymous:
    #    print (req.user.is_anonymous)
    #username = req.COOKIES.get('username','')
    #print (username)
    return render(request,'index_home.html',{'username':request.user})

def chart(req):
    return render(req,'index_home.html')

def empty(req):
    time_today= datetime.datetime.now()
    time_ye1=time_today + datetime.timedelta(days=-1)
    time_ye2=time_today + datetime.timedelta(days=-2)
    time_ye3=time_today + datetime.timedelta(days=-3)
    time_ye4=time_today + datetime.timedelta(days=-4)
    time_today=time_today.strftime("%Y-%m-%d")
    time_ye1=time_ye1.strftime("%Y-%m-%d")
    time_ye2=time_ye2.strftime("%Y-%m-%d")
    time_ye3=time_ye3.strftime("%Y-%m-%d")
    time_ye4=time_ye4.strftime("%Y-%m-%d")
    db=db_operate()
    sql_hosts="select count(*) from asset_hostlist "
    sql_hosts2="select count(*) from asset_hostlist where status='%s'" %('已装机')
    sql_hosts3="select count(*) from asset_hostlist where status='%s'" %('待装机')
    sql_messages="select count(*) from asset_message "
    sql_user="select count(*) from auth_user "
    ret1=db.select_table2(settings.OMS_MYSQL,sql_hosts)
    ret1_1=db.select_table2(settings.OMS_MYSQL,sql_hosts2)
    ret1_2=db.select_table2(settings.OMS_MYSQL,sql_hosts3)
    ret2=db.select_table2(settings.OMS_MYSQL,sql_messages)
    ret3=db.select_table2(settings.OMS_MYSQL,sql_user)
    sql_messages1="select count(*) from asset_message WHERE TO_DAYS(NOW()) = TO_DAYS(audit_time)  "
    sql_messages2="select count(*) from asset_message WHERE TO_DAYS(NOW()) - TO_DAYS(audit_time) <=2 "
    sql_messages3="select count(*) from asset_message WHERE TO_DAYS(NOW()) - TO_DAYS(audit_time) <=3 "
    sql_messages4="select count(*) from asset_message WHERE TO_DAYS(NOW()) - TO_DAYS(audit_time) <=4 "
    sql_messages5="select count(*) from asset_message WHERE TO_DAYS(NOW()) - TO_DAYS(audit_time) <=5 "
    ret_mes1=int(db.select_table2(settings.OMS_MYSQL,sql_messages1)[0])
    ret_mes2=int(db.select_table2(settings.OMS_MYSQL,sql_messages2)[0])
    ret_mes3=int(db.select_table2(settings.OMS_MYSQL,sql_messages3)[0])
    ret_mes4=int(db.select_table2(settings.OMS_MYSQL,sql_messages4)[0])
    ret_mes5=int(db.select_table2(settings.OMS_MYSQL,sql_messages5)[0])
    #return render('empty_test.html',locals())
    cpu=20
    memory=80
    return render(req,'empty_test.html',{'ret1':ret1,'ret1_1':ret1_1,'ret1_2':ret1_2,'ret2':ret2,'ret3':ret3,\
                                         'ret_mes1':ret_mes1,'ret_mes2':ret_mes2-ret_mes1,'ret_mes3':ret_mes3-ret_mes2,'ret_mes4':ret_mes4-ret_mes3,'ret_mes5':ret_mes5-ret_mes4,\
                                         'time_today':time_today,'time_ye1':time_ye1,'time_ye2':time_ye2,'time_ye3':time_ye3,'time_ye4':time_ye4,
                                         'cpu':cpu,'memory':memory})
def aqzm(req,time1=time.strftime('%Y%m%d',time.localtime(time.time()))):
    """"""
    """初始化数据库连接，游标，数据库表名"""
    db=pymysql.connect(host="192.168.0.120",user="aqzm",passwd="123456",db="aqzm",port=3306,charset="utf8")
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

    return render(req,'aqzm_test.html',{'cpu':cpu,'memory':memory,"time1":time1,'info_dict':dict_user,'dict_con':dict_con,'dict_fu':dict_fu,'info_dict2':dict_user2,'list2':list_a,'list3':list_b,'list_c':list_c,'user_con':rs_con })
def form(req):
    return render(req,'index_home.html')
def tab_panel(req):
    return render(req,'index_home.html')
def table(req):
    return render(req,'index_home.html')
def ui_elements(req):
    return render(req,'host_list.html')
def testextend(req):
    return render(req,'index_home.html')
'''def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #添加到数据库
            #User.objects.get_or_create(username = username,password = password)
            registAdd = User.objects.get_or_create(username = username,password = password)[1]
            if registAdd == False:
                #return HttpResponseRedirect('/share/')
                return render_to_response('share.html',{'registAdd':registAdd,'username':username})
            else:
                return render_to_response('share.html',{'registAdd':registAdd})

    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf})
'''
'''
def login(req):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if req.method == 'GET':
        uf = UserForm()
        return render_to_response('login.html', RequestContext(req, {'uf': uf,'nowtime': nowtime }))
    else:
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = req.POST.get('username', '')
            password = req.POST.get('password', '')
            user = User.authenticate(username = username,password = password)
            if user is not None and user.is_active:
                User.login(req,user)
                return render_to_response('index.html', RequestContext(req))
            else:
                return render_to_response('login.html', RequestContext(req, {'uf': uf,'nowtime': nowtime, 'password_is_wrong': True}))
        else:
            return render_to_response('login.html', RequestContext(req, {'uf': uf,'nowtime': nowtime }))
'''
'''
def login(req):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #对比提交的数据与数据库中的数据
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/index/')
                #将username写入浏览器cookie，失效时间为3600
                response.set_cookie('username',username,3600)
                return response
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login_test.html',{'uf':uf,'nowtime': nowtime})
#登录成功

'''
@login_required()
def index(req):
    if not req.user.is_authenticated():
        print (req.user.is_authenticated())
    username = req.COOKIES.get('username','')
    print (username)
    return render_to_response('index.html',{'username':username})
#退出登录

def logout(request):
    #response = HttpResponse('logout!!!')
    #清除cookie里保存的username
    #req.session['is_login'] = 'true'
    #req.session['user'] = ''
    #response.delete_cookie('username')
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required()
def user_list(request):
    """
    List all Hosts
    """
    #logined_username=request.COOKIES.get('username','')
    user = request.user
    user_list = User_auth.objects.all().order_by('-username')
    # host_list = HostList.objects.all()
    paginator = Paginator(user_list,3)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        user_list = paginator.page(page)
    except :
        all_user = paginator.page(paginator.num_pages)

    return render(request, 'auth_user_list.html', {'user_list': user_list, 'page': page, 'paginator':paginator,'login_user':request.user})

@login_required()
def user_list_manage(request, id=None):   # 负责添加和修改和删除主机，删除，修改主机需要提供id号
    if id:
        user_list = get_object_or_404(User_auth, pk=id)
        action = 'edit'
        # page_name = '编辑主机'
        db = db_operate()
        sql = 'select username from form_app_user where id = %s' % (id)
        ret = db.mysql_command(settings.OMS_MYSQL, sql)   # settings.OMS_MYSQL 是mysql连接参数的字典
        # 这里ret 是ip
    else:
        user_list = User_auth()
        action = 'add'
        # page_name = '新增主机'
        ret=[]

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
        if delete:
            Message.objects.create(type='user', action='manage', action_ip=ret, content='删除用户')
            user_list = get_object_or_404(User_auth, pk=id)
            user_list.delete()
            return HttpResponseRedirect(reverse('user_list'))
    if request.method == 'POST':    # 修改主机或者添加新主机
        form = UserListForm(request.POST,instance=user_list)
        #print request.POST
        operate = request.POST.get('operate')  # 这里表示点击更新了按钮
        if form.is_valid():
            if action == 'add':   #  点击添加按钮
                form.save()
                ret.append(form.cleaned_data['username'])
                Message.objects.create(type='user', action='manage', action_ip=ret, content='用户添加成功')
                return HttpResponseRedirect(reverse('user_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    Message.objects.create(type='user', action='manage', action_ip=ret, content='用户信息更新')
                    return HttpResponseRedirect(reverse('user_list'))
                else:
                    pass
    else:
        form = UserListForm(instance=user_list)

    return render(request, 'user_manager.html',
           {"form": form,
            # "page_name": page_name,
            "action": action, # 这里action 要注意 如果是edit 页面显示edit按钮 如果是add页面显示add按钮
            "login_user":request.user,
           })