import requests
import base64
from bs4 import BeautifulSoup


class LoginObj():
    def __init__(self):
        self.isLogin = False
        pass

    '''
        获取验证码
    '''
    def getCheckCodeBinary(self):
        l = requests.get('http://jwcweb1.wit.edu.cn/CheckCode.aspx')
        if l.status_code == 200:
            self.code = l.url.split('/')[-2]
            self.loginUrl = 'http://jwcweb1.wit.edu.cn/'+self.code+'/default2.aspx'
            return l.content
        else:
            return None

    '''
        重新获取验证码
    '''
    def reGetCheckCodeBinary(self):
        l = requests.get('http://jwcweb1.wit.edu.cn/'+self.code+'/CheckCode.aspx')
        if l.status_code == 200:
            return l.content
        else:
            return None

    '''
        从html中拿到__VIEWSTATE
    '''
    def __getViewState(self):
        html = requests.get(self.loginUrl)
        b = BeautifulSoup(html.text, 'xml')
        vs = b.find(name='input', attrs={'name': '__VIEWSTATE'})
        return vs.attrs['value']

    '''
        获取用户名
    '''
    def __getUserName(self):
        html = requests.get('http://jwcweb1.wit.edu.cn/'+self.sessionId+'/xs_main.aspx?xh='+self.stuNum)
        s = BeautifulSoup(html.text, 'xml')
        self.name = s.find(name='span', id='xhxm').string[:-2]


    '''
        登录
    '''
    def login(self,stuNum,password,checkCode):
        self.stuNum = stuNum
        self.password = password
        __VIEWSTATE = self.__getViewState()
        data = {
            'RatioButtonList1': '学生'.encode('gbk'),
            'TextBox2': password,
            'txtSecretCode': checkCode,
            'txtUserName': stuNum,
            '__VIEWSTATE': __VIEWSTATE,
            'Button1': '',
            'hidPdrs': '',
            'hidsc': '',
            'lbLanguege': '',
            'TextBox1': ''
        }
        headers = {
            'Host': 'jwcweb1.wit.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://jwcweb1.wit.edu.cn/'+self.code+'/default2.aspx',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '207',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.post('http://jwcweb1.wit.edu.cn/'+self.code+'/default2.aspx', data=data,
                                 headers=headers)

        if response.url.split('/')[-1] == 'default2.aspx':
            print('登录失败')
        else :
            self.sessionId = response.url.split('/')[-2]
            self.__getUserName()
            self.isLogin = True








