import requests
import json
import csv
import time
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
            date=data['created_at'].replace(" +0800 2023","")
            name=data['user']['screen_name']
            comment=data['text_raw']
            id=str(data['id'])
            ip=data['source'].replace("来自","")
            description=data['user']['description']
            gender=data['user']['gender']
            row=[no,name,ip,gender,description,date,comment]
            print(row)
            writer.writerow(row)
            no=no+1
            suburl='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id='+id+'&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id=0&count=20&uid=1776448504&locale=zh-CN'
            for j in range(0,5):
                subr=requests.get(suburl,headers=headers)
                subre=json.loads(subr.text)
                submax_id=subre['max_id']
                subdatas=subre['data']
                for subdata in subdatas:
                    subdate=subdata['created_at'].replace(" +0800 2023","")
                    subname=subdata['user']['screen_name']
                    subcomment=subdata['text_raw']
                    subip=subdata['source'].replace("来自","")
                    subdescription=subdata['user']['description']
                    subgender=subdata['user']['gender']
                    row=[no,subname,subip,subgender,subdescription,subdate,subcomment]
                    print(row)
                    writer.writerow(row)
                    no=no+1
                suburl='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id='+id+'&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id='+str(submax_id)+'&count=20&uid=1776448504&locale=zh-CN'
                time.sleep(3)
        url='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4930085347920633&is_show_bulletin=2&is_mix=0&max_id='+str(max_id)+'&count=20&uid=1776448504&fetch_level=0&locale=zh-CN'
        time.sleep(3)
        if no>=5000:
            break
    f.close()