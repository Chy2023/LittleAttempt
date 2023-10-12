import requests
import json
import csv
import time
#该模块用来从微博爬取评论数据
#定义一个类，用来收集数据、对原始数据做一定处理
class Data:
    def __init__(self,data):
        self.date=data['created_at'].replace(" +0800 2023","")
        self.name=data['user']['screen_name']
        self.comment=data['text_raw']
        self.ip=data['source'].replace("来自","")
        self.description=data['user']['description']
        self.gender=data['user']['gender']
    #方便将数据写入csv文件
    def Row(self,no):
        row=[no,self.name,self.ip,self.gender,self.description,self.date,self.comment]
        return row
#通过相邻评论页面的逻辑关系，循环获取评论；具体逻辑见实验报告
def GetComment(headers,url):
    no=1
    head = ['NO','NAME','IP','GENDER','DESCRIPTION','DATE','COMMENT']
    f=open("hw2.csv","w",newline='',encoding='utf_8')
    writer=csv.writer(f)
    writer.writerow(head)
    for i in range(0,15):
        r=requests.get(url,headers=headers)
        re=json.loads(r.text)
        max_id=re['max_id']
        datas=re['data']
        for data in datas:
            item=Data(data)
            row=item.Row(no)
            #print(row)
            writer.writerow(row)
            no=no+1
            id=str(data['id'])
            suburl='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id='+id+'&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id=0&count=20&uid=1776448504&locale=zh-CN'
            for j in range(0,5):
                subr=requests.get(suburl,headers=headers)
                subre=json.loads(subr.text)
                submax_id=subre['max_id']
                subdatas=subre['data']
                for subdata in subdatas:
                    item=Data(subdata)
                    row=item.Row(no)
                    #print(row)
                    writer.writerow(row)
                    no=no+1
                suburl='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id='+id+'&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id='+str(submax_id)+'&count=20&uid=1776448504&locale=zh-CN'
                time.sleep(3)
        url='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4930085347920633&is_show_bulletin=2&is_mix=0&max_id='+str(max_id)+'&count=20&uid=1776448504&fetch_level=0&locale=zh-CN'
        time.sleep(3)
        if no>=5000:
            break
    f.close()