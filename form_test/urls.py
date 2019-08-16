"""form_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from form_app import views as form_app_views
from django.conf import settings ##new
from django.conf.urls.static import static ##new
from asset import views as asset_views
from deploy import views as deploy_views
from xtgl import views as xtgl_views

urlpatterns = [
    path('admin/', admin.site.urls),
    ##form_app  app
    path('',form_app_views.login,name='login'),
    path('login/',form_app_views.login,name='login'),
    path('register/',form_app_views.register,name='register'),
    # path('index/',form_app_views.index,name='index'),
    path('logout/',form_app_views.logout,name='logout'),
    path('chart/', form_app_views.chart,name='chart'),
    path('form/', form_app_views.form,name='form'),
    path('tab_panel/', form_app_views.tab_panel,name='tabsspanel'),
    path('table/', form_app_views.table,name='table'),
    path('ui_elements/', form_app_views.ui_elements,name='uisselements'),
    path('empty/', form_app_views.empty,name='empty'),
    path('testextend/', form_app_views.testextend,name='testextend'),
    path('user/user_list/', form_app_views.user_list, name='user_list'),
    path('user/add_user/', form_app_views.user_list_manage, name='add_user'),
    path('index/', form_app_views.test,name='index'),
    ##asset app
    path('asset/record/', asset_views.record, name='record'),
    path('asset/host_list/', asset_views.host_list, name='host_list'),
    path('asset/add_host/', asset_views.host_list_manage, name='add_host'),
    path('asset/host_manage/(?P<id>\d+)/', asset_views.host_list_manage, name='host_manage'),
    path('asset/delete_host/', asset_views.host_list_manage, name='host_delete'),
    path('user/user_manage/(?P<id>\d+)/', form_app_views.user_list_manage, name='user_manage'),
    path('user/delete_user/', form_app_views.user_list_manage, name='user_delete'),
    ##deploy app
    path('deploy/key_list/', deploy_views.salt_key_list, name='key_list'),
    path('deploy/key_delete/', deploy_views.salt_delete_key, name='delete_key'),
    path('deploy/key_accept/', deploy_views.salt_accept_key, name='accept_key'),
    path('deploy/module_deploy/', deploy_views.module_deploy, name='module_deploy'),
    path('deploy/remote_execution/', deploy_views.remote_execution, name='remote_execution'),
    path('deploy/targeting_execution/', deploy_views.targeting_execution, name='targeting_execution'),
    ##xtgl app
    path('aqzm/', xtgl_views.aqzm,name='aqzm'),
    path('aqzm/(?P<time1>\d{8})/', xtgl_views.aqzm,name='aqzm'),
    path('aqzm_index/', xtgl_views.aqzm_index,name='aqzm_index'),
    path('mac/mac_list/',xtgl_views.mac_list,name='mac_list'),
    path('mac/add_mac/',xtgl_views.mac_list,name='add_mac'),
    path('mac/mac_manage/(?P<id>\d+)/',xtgl_views.mac_list,name='mac_manage'),
]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) ##new
