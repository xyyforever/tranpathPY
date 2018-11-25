import time
import requests
import re,json

class TaoBao:

    def __init__(self):
        # 淘宝登录的URL
        self.login_url = "https://login.taobao.com/member/login.jhtml"
        # 登陆前的验证,以获取cookie用于后续的登陆操作
        self.st_url = 'https://login.taobao.com/member/vst.htm?st={st}'
        # 淘宝登陆用户名
        self.username = '17621368758'
        #header信息  (设置几个基本就可以的了，没必要设置这么多)
        self.loginHeaders = {
            'Host':'login.taobao.com',
            'Connection':'keep-alive',
            'Content-Length':'3357',
            'Cache-Control':'max-age=0',
            'Origin':'https://login.taobao.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer':'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        }
        #可重复使用的ua,可以使用抓包软件在实现一次登陆之后获得
        self.ua = '114#tpgoZGQUTTo8UWbrhs90BCPGXQQ8dPnKhZ39isDcII979I3p1An7NfxLY4bgHtgSWrmyccKIJCKcJcax4AsSOEltiWO7SFpm3zjcHrONf8BEpBxz/huGVZejn/9WZhdsGcVp4ZkSW9p0UaIkMmWoOA0CYGSOQHsuQD1Tjs82wbYFokga35TawR18eTmbn8TbsQ7wfTsnnTb8z6gm8bsTbYDSyUxxBgoSJt2OZTZXTbzz+M8mTc+TCRJNsoTXAzj32FemIssNnRu8s6ldzwlsonRrfnIT4IZMaQ6rGsTXnbAZ0nl0ITjsTwfml3MTlqTs7wuyf6wWX8TU26008RUTdC7yZ6ITsPk6265afTsnTTTU1MzwTmIonjuKZ6oW8TTT2/rmsAmjskFnLj1srJndMvXM0+bPEhJHc80atUfzHVzGx15vg3NEYARhgAbVC+aEXvl/yWT+fQrWjZN4GQ08DYmEWIodv9YHQI1CyatBt1fS2jg1QJyPYIJQPyk6EGvHuNv+jcdidFa7DXE8aDAyul+wX65lP/NZur0XhXOW5C6DSjEj6Wjm2HUeSxMePpHCyHzc21tLTLjGY9PSXBobJ2F7ltaXU9xYSheMKGHOhjbm9vOJafRmdWImN8sO2Cebl27HaI+msDkgM+2A9irLEDXB70i1je/jzsvqc8vojwVhSATCwamzNOuYx2MOsgOjkcKiNluZ0FYZDd1BfM9y9M6GoiNnnrw5CLq/jfGVCatx80qkqHzCighA71+m+tOtvvlXnoc57Z1aixlvYaMMvvDT6oopdPNs8jnneRS1hqbiLosjKDp4jAzVMtwCx2PAx9PbHWVekACbfvJxv+NF8Lj2pJrA9y9B+TdqkiLyeroam1O0yXpMXUbCZbZPLaB1b3ApEFVQMqo8LmKSxZ3oo6tgV8vi8PmBxycUV+rZAhRyBGTeLPa44xqZS7Gxv3ySLN/ssVd9akaRey3H5tEslT1s0ob59kKeGb54u6yKNaacR79Dj2hQ'
        #将你输入的密码经过算法计算后提交,暂时不知道如何从js中获取,只能用笨方法从正确登陆后的表单中提取了
        self.TPL_password2 = '7f4e576bf919953a0cca4763e501152abf36c474211772e43a30a1e89550b7e2824a10e6958bad39e4286c1506c439ca5e84a0f43ef7591a562b9ad29fd5e63809d9269939b72723170dd95ff86b619c03803b04a629edef6f50b0af35c8c71032d27b8d3885bfb65d716cb92ed3ea32a764287284fed06b113587eef499689e'
        #POST提交页面时所提交的表单数据
        self.post = {
            'TPL_username':self.username,
            'TPL_password': '',
            'ncoSig': '',
            'ncoSessionid': '',
            'ncoToken': '35afb8c178caecc65d4db8d0cdcf55cb63316049',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'newlogin': '0',
            'loginsite': '0',
            'TPL_redirect_url': "https://i.taobao.com/my_taobao.htm?",
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'css_style': '',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'tid': '',
            'loginType': '3',
            'minititle': '',
            'minipara': '',
            'pstrong': '',
            'sign': '',
            'need_sign': '',
            'isIgnore': '',
            'full_redirect': '',
            'sub_jump': '',
            'popid': '',
            'callback': '',
            'guf': '',
            'not_duplite_str ': '',
            'need_user_id': '',
            'poy': self.TPL_password2,
            'gvfdcname': '10',
            'gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61317A30392E322E3735343839343433372E372E3333633532653864725951795A5926663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246627579657274726164652E74616F62616F2E636F6D25324674726164652532466974656D6C6973742532466C6973745F626F756768745F6974656D732E68746D253346',
            'from_encoding': '',
            'sub': '',
            'TPL_password_2':self.TPL_password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp': '',
            'oslanguage': 'zh-CN',
            'sr': '1920*1080',
            'osVer': 'windows|6.1',
            'naviVer': 'chrome|64.03282186',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'nickLoginLink': '',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?&useMobile=true',
            'showAssistantLink': '',
            'um_token': 'HV01PAAZ0b8705a865692b795aaf7d1b0022d8c0',
            'ua': self.ua
        }
        #设置cookie
        self.cookies = {}
        #请求登录
        print('-------请求登陆-------')

    def _get_st_token_url(self):
        response = requests.post(self.login_url, self.post, self.loginHeaders,cookies=self.cookies,verify=False)
        content = response.content.decode('gbk')
        st_token_url_re = re.compile(r'<script src=\"(.*)\"><\/script>')
        match_url = st_token_url_re.findall(content)
        if match_url:
            st_token_url = match_url[0]
            return st_token_url
        else:
            print('请检查是否匹配成功')

    def _get_st_token(self):
        st_token_url = self._get_st_token_url()
        st_response = requests.get(st_token_url,verify=False)
        st_response_content = st_response.content.decode('gbk')
        st_token_re = re.compile(r'"data":{"st":"(.+)"}')
        match_st_token_list = st_token_re.findall(st_response_content)
        if match_st_token_list:
            st = match_st_token_list[0]
            return st
        else:
            print('请检查是否匹配成功')

    def login_by_st(self,):
        st = self._get_st_token()
        st_url =self.st_url.format(st=st)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive'
        }
        response = requests.get(st_url, headers=headers, verify=False)
        content = response.content.decode('gbk')
        self.cookies = response.cookies   #这一步是必须要做的
        # 检测结果，看是否登录成功
        pattern = re.compile('top.location.href = "(.*?)"', re.S)
        match = re.search(pattern, content)
        if match:
            print(u'登录网址成功')
            return match
        else:
            print(u'登录失败')
            return False

    def _request_ware(self,ware_name, price_start, price_end):
        try:
            #登陆
            self.login_by_st()
            taobao_url = 'https://s.taobao.com/search'
            datas = []
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'referer': 'https://www.taobao.com/?spm=0.1.1581860521.1.7483523cnmVQ2I',
            }
            for i in range(2):
                payload = {
                    'q': ware_name,
                    'filter': 'reserve_price[%d,%d]' %(price_start,price_end),
                    'ie': 'utf-8',
                    'data-key': 's',
                    'data-value': i*44
                }
                response = requests.get(taobao_url, headers=headers, params=payload, verify = False, cookies = self.cookies)
                data = response.text.encode('utf-8').decode('utf-8')

                datas.append(data)
            return datas
        except Exception as e:
            print(e)

    def _parse(self,datas):
        ware_list = []
        for d in datas:
            print(d)
            print(type(d))
            data = re.search('"auctions".*"recommendAuctions"', d, re.S).group()
            aa = data[11:-20]
            json_aa = json.loads(aa)
            ware_list.extend(json_aa)
        return ware_list









# if __name__ == '__main__':
#     tb = TaoBao()
#     datas = tb._request_ware(ware_name='乐高',price_start=100,price_end=1000)
#     ware_list = tb._parse(datas)
#     ware_pro = ['raw_title', 'detail_url', 'view_price', 'item_loc', 'view_sales', 'nick']
#     wares = map(lambda x: dict([(key, x[key]) for key in ware_pro]), ware_list)
#     print(list(wares))