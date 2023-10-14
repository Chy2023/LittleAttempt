import requests
import json
import csv
import time
#This module is used to crawl comment data from microblog
#Define a class that collects data and does something with the raw data
class Data:
    def __init__(self,data):
        self.date=data['created_at'].replace(" +0800 2023","")
        self.name=data['user']['screen_name']
        self.comment=data['text_raw']
        self.ip=data['source'].replace("来自","")
        self.description=data['user']['description']
        self.gender=data['user']['gender']
    #Easy to write data to csv file
    def Row(self,no):
        row=[no,self.name,self.ip,self.gender,self.description,self.date,self.comment]
        return row
#Through the logical relationship of adjacent comment pages, the review is obtained in a loop. 
#See the experiment report for specific logic
def GetComment(headers,url):
    no=1
    head = ['NO','NAME','IP','GENDER','DESCRIPTION','DATE','COMMENT']
    f=open("KUN\hw2.csv","w",newline='',encoding='utf_8')
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