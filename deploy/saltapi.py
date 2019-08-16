__author__ = 'Administrator'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""


#import urllib2 //python3.6 urllib2 被urllib.request取代
import urllib
import urllib.parse
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

try:
    import json
except ImportError:
    import simplejson as json


class SaltAPI(object):
    __token_id = ''

    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password

    def token_id(self):
        ''' user login and get token id '''
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.parse.urlencode(params)
        obj = urllib.parse.unquote(encode).encode('UTF8')
        content = self.postRequest(obj, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def postRequest(self, obj, prefix='/'):
        """
        返回json格式
        :param obj:
        :param prefix:
        :return:
        """
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, obj, headers)
        opener = urllib.request.urlopen(req)
        content = json.loads(opener.read().decode('utf-8'))
        return content

    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre  # minions_pre代表没有接受的主机

    def delete_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def remote_noarg_execution(self, tgt, fun):
        ''' Execute commands without parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

    def remote_execution(self, tgt, fun, arg):
        ''' Command execution with parameters '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0][tgt]
        return ret

    '''new add'''
    def remote_ssh(self,fun,arg):
        params = {'client': 'local', 'tgt': '192.168.1.120', 'fun': fun, 'arg': arg}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['192.168.1.120']
        return ret

    def target_remote_execution(self, tgt, fun, arg):
        ''' Use targeting for remote execution '''
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid

    def deploy(self, tgt, arg):
        ''' Module deployment '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        return content

    def async_deploy(self, tgt, arg=None):
        ''' Asynchronously send a command to connected minions '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        # print content
        jid = content['return'][0]['jid']
        # print jid
        return jid

    def target_deploy(self, tgt, arg):
        ''' Based on the node group forms deployment '''
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'nodegroup'}
        obj = urllib.parse.urlencode(params).encode(encoding='UTF8')
        self.token_id()
        content = self.postRequest(obj)
        jid = content['return'][0]['jid']
        return jid


def main():
    url = 'https://192.168.1.120:8888'
    # token = '204f7d1a4bd2e098be379b93a203fe84295f5256'
    #sapi = SaltAPI(url=url, username='test', password='test')
    #print (sapi.token_id())
    #print (sapi.list_all_key())
    # sapi.delete_key('test-01')
    # sapi.accept_key('test-01')
    # sapi.deploy_1('test-01','nginx')
    #print (sapi.async_deploy('zabbix-agent', 'nginx'))


if __name__ == '__main__':
    main()
