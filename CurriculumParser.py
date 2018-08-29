from bs4 import BeautifulSoup
from bs4.element import NavigableString
import json
import requests
from LoginObj import LoginObj


# 课程信息类
class CourseInfo(object):

    def __init__(self, week, start, end, info):
        self.week = week
        self.start = start
        self.end = end
        self.info = info

'''
    登录后爬课程表类
'''
class CurriculumParser():

    def __init__(self,loginObj):
        self.loginObj = loginObj
        if not self.loginObj.isLogin:
            raise Exception('未登录')

    '''
        将爬到的html转为json接口
    '''
    def __convertHtml2Json(self,html):



        #课程表
        curriculum = {}
        table = BeautifulSoup(html.replace("""<br>""",'\n'), 'html.parser').find('table',attrs={'id':'Table6'})
        i = -2
        #记录当前遍历到了第几节课
        current = [0, 1, 1, 1, 1, 1, 1, 1]

        #遍历html表格的每一行
        for tr in table.children:
            # 过滤掉多余换行符
            if not isinstance(tr, NavigableString):
                i += 1
                if i == 0 or i == -1:
                    continue
                week = 1
                for td in tr:
                    while current[week] > i:
                        week += 1
                        if week > 7:
                            break
                    #过滤掉多余换行符
                    if not isinstance(td, NavigableString) and td.has_attr('align'):
                        #没课不添加
                        if td.text == ' ':
                            current[week] += 1
                        #有课
                        else:
                            if td.has_attr('rowspan'):
                                #课程时长
                                l = int(td.attrs['rowspan'])
                                course = td.text
                                split = course.find('\n')
                                c = CourseInfo(week, current[week], current[week] + l - 1, course[split+1:])
                                name = course[:split]
                                if name in curriculum.keys():
                                    curriculum[name].append(c)
                                else:
                                    curriculum[name] = [c]
                                current[week] += l
        print(json.dumps(curriculum, default=lambda obj: obj.__dict__, ensure_ascii=False))
        return json.dumps(curriculum, default=lambda obj: obj.__dict__, ensure_ascii=False)


    '''
        爬取课程表html
    '''
    def getCurriculum(self):
        headers = {
            'Host': 'jwcweb1.wit.edu.cn',
            'User-Agent': 'Mozilla/5.0(X11;Ubuntu;Linuxx86_64;rv:61.0)Gecko/20100101Firefox/61.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;,q = 0.9,*/*;q = 0.8',
            'Accept-Language': 'en-GB,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://jwcweb1.wit.edu.cn/'+
                       self.loginObj.sessionId+'/xs_main.aspx?xh='+self.loginObj.stuNum,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        url = 'http://jwcweb1.wit.edu.cn/'+self.loginObj.sessionId+'/tjkbcx.aspx?xh='+self.loginObj.stuNum+'&xm='+str(self.loginObj.name.encode('gbk'))+'&gnmkdm=N121601'
        curriculum = requests.get(url,headers=headers)
        json_curriculum = self.__convertHtml2Json(curriculum.text)
        return json_curriculum


'''
    测试代码
'''
if __name__ == '__main__':
    l = LoginObj()
    file = open('/home/clay/桌面/a.gif', 'wb')
    file.write(l.getCheckCodeBinary())
    file.close()
    checkCode = input()
    l.login('1610010327', 'zy123456789zy', checkCode)
    if l.isLogin:
        print(l.name)
    cp = CurriculumParser(l)
    cp.getCurriculum()
