import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import json
import random


html = """
<table class="datelist" cellspacing="0" cellpadding="3" border="0" id="Datagrid1" style="DISPLAY:block">
	<tr class="datelisthead">
		<td><a href="javascript:__doPostBack('Datagrid1$_ctl1$_ctl0','')">学年</a></td><td><a href="javascript:__doPostBack('Datagrid1$_ctl1$_ctl1','')">学期</a></td><td><a href="javascript:__doPostBack('Datagrid1$_ctl1$_ctl2','')">课程代码</a></td><td><a href="javascript:__doPostBack('Datagrid1$_ctl1$_ctl3','')">课程名称</a></td><td>课程性质</td><td>课程归属</td><td>学分</td><td>绩点</td><td>成绩</td><td>辅修标记</td><td>补考成绩</td><td>重修成绩</td><td>开课学院</td><td>备注</td><td>重修标记</td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>05B20012</td><td>计算机程序设计基础(2)</td><td>必修课</td><td>&nbsp;</td><td>4.0</td><td>   3.40</td><td>84</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与工程学院</td><td></td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>05B60010</td><td>认识实习</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   3.50</td><td>85</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与工程学院</td><td></td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>09B10102</td><td>高等数学A2</td><td>必修课</td><td>&nbsp;</td><td>6.0</td><td>   2.60</td><td>76</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>理学院</td><td></td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>10B20021</td><td>综合英语(2)</td><td>必修课</td><td>&nbsp;</td><td>4.0</td><td>   2.10</td><td>71</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>外语学院</td><td></td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>10B20460</td><td>英语语法</td><td>必修课</td><td>&nbsp;</td><td>1.5</td><td>   1.00</td><td>60</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>外语学院</td><td></td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>10B20472</td><td>英语听力与口语(2)</td><td>必修课</td><td>&nbsp;</td><td>3.0</td><td>   1.50</td><td>65</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>外语学院</td><td></td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>10B20481</td><td>英语阅读与写作(1)</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   1.10</td><td>61</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>外语学院</td><td></td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>10B60100</td><td>名著研读</td><td>必修课</td><td>&nbsp;</td><td>3.0</td><td>   2.60</td><td>76</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>外语学院</td><td></td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>11B10211</td><td>大一体育(乒乓球)</td><td>全校性公选课</td><td>全校性公选课</td><td>1.5</td><td>   3.20</td><td>82</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>体育部</td><td></td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>23B10020</td><td>中国近现代史纲要</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   2.60</td><td>76</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>马克思主义学院</td><td></td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>23B10030</td><td>马克思主义基本原理概论</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   3.90</td><td>89</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>马克思主义学院</td><td></td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>23B10110</td><td>形势政策与廉洁教育</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   3.50</td><td>85</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>马克思主义学院</td><td></td><td></td>
	</tr>
</table>
"""
class Grade():

    def __init__(self,code,name,type,score,gpa,grade,isMinored,makeup,second,academy,isSecond):
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


soup = BeautifulSoup(html,'html.parser')
gradeTable = soup.find('table',attrs={'class':'datelist'})
gradeList = {
    'year': None,
    'term':None,
    'grade' : []
}

i = 1
"""
<td>2016-2017</td>
<td>2</td>
<td>05B20012</td>
<td>计算机程序设计基础(2)</td>
<td>必修课</td>
<td> </td>
<td>4.0</td>
<td>   3.40</td>
<td>84</td>
<td>0</td>
<td> </td>
<td> </td>
<td>计算机科学与工程学院</td>
<td></td>
<td></td>
"""

for tr in gradeTable.children:

    if isinstance(tr,NavigableString):
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
              tr.contents[8].string,
              tr.contents[9].string,
              tr.contents[10].string,
              tr.contents[11].string,
              tr.contents[12].string,
              tr.contents[13].string,
              tr.contents[14].string)
    gradeList['grade'].append(g)
print(json.dumps(gradeList,default=lambda obj:obj.__dict__,ensure_ascii=False))

