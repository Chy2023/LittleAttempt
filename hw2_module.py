import requests
import json
import csv
import time
def GetComment(headers,url):
    no=1
    head = ['NO','NAME','ID','DATE','COMMENT']
    f=open("hw2.csv","w",newline='',encoding='utf_8')
    writer=csv.writer(f)
    writer.writerow(head)
    for i in range(0,15):
        r=requests.get(url,headers=headers)
        re=json.loads(r.text)
        max_id=re['max_id']
        datas=re['data']
        for data in datas:
            date=data['created_at']
            name=data['user']['screen_name']
            comment=data['text_raw']
            id=str(data['id'])
            print(str(no)+'  '+name+'  '+id+'  '+date+":")
            print(comment)
            row=[no,name,id,date,comment]
            writer.writerow(row)
            no=no+1
            suburl='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id='+id+'&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id=0&count=20&uid=1776448504&locale=zh-CN'
            for j in range(0,5):
                subr=requests.get(suburl,headers=headers)
                subre=json.loads(subr.text)
                submax_id=subre['max_id']
                subdatas=subre['data']
                for subdata in subdatas:
                    subdate=subdata['created_at']
                    subname=subdata['user']['screen_name']
                    subcomment=subdata['text_raw']
                    subid=str(subdata['id'])
                    print(str(no)+'  '+subname+'  '+subid+'  '+subdate+":")
                    print(subcomment)
                    row=[no,subname,subid,subdate,subcomment]
                    writer.writerow(row)
                    no=no+1
                suburl='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id='+id+'&is_show_bulletin=2&is_mix=1&fetch_level=1&max_id='+str(submax_id)+'&count=20&uid=1776448504&locale=zh-CN'
                time.sleep(3)
        url='https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4930085347920633&is_show_bulletin=2&is_mix=0&max_id='+str(max_id)+'&count=20&uid=1776448504&fetch_level=0&locale=zh-CN'
        time.sleep(3)
    f.close()
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
         'Cookie':'PC_TOKEN=59cabbbb88; WBStorage=4d96c54e|undefined; XSRF-TOKEN=YJx9XBZCyuoCwJFxm91Vgrkj; login_sid_t=03566ca35ae6f943cd73cd4c61f52fb6; cross_origin_proto=SSL; SUB=_2A25IHQvTDeRhGeFG6FMU-CvLyj6IHXVra3obrDV8PUNbmtANLUelkW9NecUdv1uYwh1bMUAllC2khsLX8oABS1mQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFz63TW03M.ARM0zZ_gaLGB5JpX5KzhUgL.FoMRe02f1h-NeKz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1hepSKnfS02E; ALF=1727704835; SSOLoginState=1696168835; WBPSESS=DlY_SWmwvJp1UZxDBneCv_ke7fxA6M_MywSlrIHS0WsvSA_qFpixWhIFrmcTa9sKb7g6LurcZUDS3eIOAr_fPan-ZoOI4BkjVzN1s1METW4z42PyrpD4jERHQOKpSeD91o4xA2etctBcoji8k36REA==',
         'Referer':'https://weibo.com/1784473157/NlSDGmf4F'}
url="https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4930085347920633&is_show_bulletin=2&is_mix=0&count=10&uid=1776448504&fetch_level=0&locale=zh-CN"
#GetComment(headers,url)