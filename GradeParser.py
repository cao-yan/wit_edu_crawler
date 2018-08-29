import requests
from bs4 import BeautifulSoup
from LoginObj import LoginObj
from bs4.element import NavigableString
import json

#单个课程分数类
class Grade():
    def __init__(self, code, name, type, score, gpa, grade, isMinored, makeup, second, academy, isSecond):
        self.code = code
        self.name = name
        self.type = type
        self.score = score
        self.gpa = gpa
        self.grade = grade
        self.isMinored = isMinored
        self.makeup = makeup
        self.second = second
        self.academy = academy
        self.isSecond = isSecond


'''
    爬取学生成绩类
'''
class GradeParser(object):

    def __init__(self,loginObj):
        self.loginObj = loginObj
        if not self.loginObj.isLogin:
            raise Exception('未登陆')

    '''
        从html中拿到__VIEWSTATE
    '''
    def __getViewState(self):
        headers = {
            'Host': 'jwcweb1.wit.edu.cn',
            'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linuxx86_64;rv:61.0)Gecko/20100101Firefox/61.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;,q = 0.9,*/*;q = 0.8',
            'Accept-Language': 'en-GB,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://jwcweb1.wit.edu.cn/'+self.loginObj.sessionId+'/xs_main.aspx?xh='+self.loginObj.stuNum,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        html = requests.get(
            'http://jwcweb1.wit.edu.cn/'+self.loginObj.sessionId+'/xscjcx.aspx?xh='+
            self.loginObj.stuNum+'&xm='+
            str(self.loginObj.name.encode('gbk'))+'&gnmkdm=N121617',
            headers=headers)
        soup = BeautifulSoup(html.text, 'xml')
        a = soup.find('form', attrs={'name': 'Form1'}).find('input', attrs={'name': '__VIEWSTATE'})
        self.__VIEWSTATE = a['value']
        print(self.__VIEWSTATE)

    def convertHtml2Json(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        gradeTable = soup.find('table', attrs={'class': 'datelist'})
        gradeList = {
            'year': None,
            'term': None,
            'grade': []
        }

        i = 1
        for tr in gradeTable.children:

            if isinstance(tr, NavigableString):
                continue
            if i == 1:
                i = 0
                continue
            if i == 0:
                i = -1
                gradeList['year'] = tr.contents[1].string
                gradeList['term'] = tr.contents[2].string
            g = Grade(tr.contents[3].string,
                      tr.contents[4].string,
                      tr.contents[5].string,
                      tr.contents[7].string,
                      tr.contents[8].string.strip(),
                      tr.contents[9].string,
                      tr.contents[10].string,
                      tr.contents[11].string,
                      tr.contents[12].string,
                      tr.contents[13].string,
                      tr.contents[14].string)
            gradeList['grade'].append(g)
        return json.dumps(gradeList, default=lambda obj: obj.__dict__, ensure_ascii=False)

    def getGrade(self):
        headers = {
            'Host': 'jwcweb1.wit.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://jwcweb1.wit.edu.cn/'+
                       self.loginObj.sessionId+'/xscjcx.aspx?xh='+
                       self.loginObj.stuNum+'&xm='+
                       '%B2%DC%D1%D7'+'&gnmkdm=N121617',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '4363',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        data = {
            '__EVENTARGUMENT':'',
            '__EVENTTARGET':'',
            '__VIEWSTATE':'dDwtOTM3MjY4MTUzO3Q8cDxsPFNvcnRFeHByZXM7c2ZkY2JrO2RnMztkeWJ5c2NqO1NvcnREaXJlO3hoO3N0cl90YWJfYmpnO2NqY3hfbHNiO3p4Y2pjeHhzOz47bDxrY21jO1xlO2JqZztcZTthc2M7MTYxMDE0MDEwMTt6Zl9jeGNqdGpfMTYxMDE0MDEwMTs7MDs+PjtsPGk8MT47PjtsPHQ8O2w8aTw0PjtpPDEwPjtpPDE5PjtpPDI0PjtpPDMyPjtpPDM2PjtpPDM4PjtpPDQwPjtpPDQyPjtpPDQ0PjtpPDQ2PjtpPDQ4PjtpPDUwPjtpPDU0PjtpPDU2PjtpPDU4Pjs+O2w8dDx0PHA8cDxsPERhdGFUZXh0RmllbGQ7RGF0YVZhbHVlRmllbGQ7PjtsPFhOO1hOOz4+Oz47dDxpPDM+O0A8XGU7MjAxNy0yMDE4OzIwMTYtMjAxNzs+O0A8XGU7MjAxNy0yMDE4OzIwMTYtMjAxNzs+Pjs+Ozs+O3Q8dDxwPHA8bDxEYXRhVGV4dEZpZWxkO0RhdGFWYWx1ZUZpZWxkOz47bDxrY3h6bWM7a2N4emRtOz4+Oz47dDxpPDc+O0A85b+F5L+u6K++O+mAieS/ruivvjvlhajmoKHmgKflhazpgInor7475qCh6YCJ5L+u6K++O+WFqOagoeaAp+S7u+mAieivvjvliJvmlrDmlZnogrLor747XGU7PjtAPDAxOzAyOzAzOzA0OzA1OzA2O1xlOz4+Oz47Oz47dDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Oz47Oz47dDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Oz47Oz47dDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcZTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDtWaXNpYmxlOz47bDzlrablj7fvvJoxNjEwMTQwMTAxO288dD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w85aeT5ZCN77ya5pu554KOO288dD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w85a2m6Zmi77ya5aSW6K+t5a2m6ZmiO288dD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w85LiT5Lia77yaO288dD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w86Iux6K+t77yL6L2v5Lu25bel56iLO288dD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOS4k+S4muaWueWQkTo7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w86KGM5pS/54+t77yaMjAxNuiLseivre+8i+i9r+S7tuW3peeoizE7bzx0Pjs+Pjs+Ozs+O3Q8QDA8cDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+Pjs+Ozs7Ozs7Ozs7Oz47Oz47dDw7bDxpPDE+O2k8Mz47aTw1PjtpPDc+O2k8OT47aTwxMz47aTwxNT47aTwxNz47aTwyMT47aTwyMz47aTwyND47aTwyNT47aTwyNz47aTwyOT47aTwzMT47aTwzMz47aTwzNT47aTw0Mz47aTw0OT47aTw1Mz47aTw1ND47PjtsPHQ8cDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+Pjs+Ozs+O3Q8QDA8cDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+PjtwPGw8c3R5bGU7PjtsPERJU1BMQVk6bm9uZTs+Pj47Ozs7Ozs7Ozs7Pjs7Pjt0PDtsPGk8MTM+Oz47bDx0PEAwPDs7Ozs7Ozs7Ozs+Ozs+Oz4+O3Q8cDxwPGw8VGV4dDtWaXNpYmxlOz47bDzoh7Pku4rmnKrpgJrov4for77nqIvmiJDnu6nvvJo7bzx0Pjs+Pjs+Ozs+O3Q8QDA8cDxwPGw8UGFnZUNvdW50O18hSXRlbUNvdW50O18hRGF0YVNvdXJjZUl0ZW1Db3VudDtEYXRhS2V5czs+O2w8aTwxPjtpPDE+O2k8MT47bDw+Oz4+O3A8bDxzdHlsZTs+O2w8RElTUExBWTpibG9jazs+Pj47Ozs7Ozs7Ozs7PjtsPGk8MD47PjtsPHQ8O2w8aTwxPjs+O2w8dDw7bDxpPDA+O2k8MT47aTwyPjtpPDM+O2k8ND47aTw1PjtpPDY+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPDEwQjIwMDExOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDznu7zlkIjoi7Hor60oMSk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOW/heS/ruivvjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Mi4wOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDw1NTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85a2m56eR5Z+656GA6K++Oz4+Oz47Oz47Pj47Pj47Pj47dDxAMDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+O3A8bDxzdHlsZTs+O2w8RElTUExBWTpub25lOz4+Pjs7Ozs7Ozs7Ozs+Ozs+O3Q8QDA8Ozs7Ozs7Ozs7Oz47Oz47dDxAMDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+O3A8bDxzdHlsZTs+O2w8RElTUExBWTpub25lOz4+Pjs7Ozs7Ozs7Ozs+Ozs+O3Q8QDA8Ozs7Ozs7Ozs7Oz47Oz47dDxAMDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+O3A8bDxzdHlsZTs+O2w8RElTUExBWTpub25lOz4+Pjs7Ozs7Ozs7Ozs+Ozs+O3Q8QDA8cDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+PjtwPGw8c3R5bGU7PjtsPERJU1BMQVk6bm9uZTs+Pj47Ozs7Ozs7Ozs7Pjs7Pjt0PEAwPHA8cDxsPFZpc2libGU7PjtsPG88Zj47Pj47Pjs7Ozs7Ozs7Ozs+Ozs+O3Q8QDA8cDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+PjtwPGw8c3R5bGU7PjtsPERJU1BMQVk6bm9uZTs+Pj47Ozs7Ozs7Ozs7Pjs7Pjt0PEAwPHA8cDxsPFZpc2libGU7PjtsPG88Zj47Pj47cDxsPHN0eWxlOz47bDxESVNQTEFZOm5vbmU7Pj4+Ozs7Ozs7Ozs7Oz47Oz47dDxAMDw7QDA8OztAMDxwPGw8SGVhZGVyVGV4dDs+O2w85Yib5paw5YaF5a65Oz4+Ozs7Oz47QDA8cDxsPEhlYWRlclRleHQ7PjtsPOWIm+aWsOWtpuWIhjs+Pjs7Ozs+O0AwPHA8bDxIZWFkZXJUZXh0Oz47bDzliJvmlrDmrKHmlbA7Pj47Ozs7Pjs7Oz47Ozs7Ozs7Ozs+Ozs+O3Q8cDxwPGw8VGV4dDtWaXNpYmxlOz47bDzmnKzkuJPkuJrlhbEyM+S6ujtvPGY+Oz4+Oz47Oz47dDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Oz47Oz47dDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Oz47Oz47dDxwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxXSVQ7Pj47Pjs7Pjt0PHA8cDxsPEltYWdlVXJsOz47bDwuL2V4Y2VsLzE2MTAxNDAxMDEuanBnOz4+Oz47Oz47Pj47dDw7bDxpPDM+Oz47bDx0PEAwPDs7Ozs7Ozs7Ozs+Ozs+Oz4+Oz4+Oz4+Oz6Sf8zZnR5j8m5o/1fEhV7TBCjwvw==',
            'btn_xq':'学期成绩'.encode('gbk'),
            'ddl_kcxz':'',
            'ddlXN':'2016-2017',
            'ddlXQ':'2',
            'hidLanguage':''
        }
        url = 'http://jwcweb1.wit.edu.cn/'+self.loginObj.sessionId+'/xscjcx.aspx?xh='+self.loginObj.stuNum+'&xm='+'%B2%DC%D1%D7'+'&gnmkdm=N121617'
        grade = requests.post(url,headers = headers,data=data)
        return self.convertHtml2Json(grade.text)

'''
    测试代码
'''
if __name__ == '__main__':
    l = LoginObj()
    file = open('/home/clay/桌面/a.gif', 'wb')
    file.write(l.getCheckCodeBinary())
    file.close()
    checkCode = input()
    l.login('1610140101', 'cy123.', checkCode)
    if l.isLogin:
        print(l.name)
        cp = GradeParser(l)
        cp.getGrade()
