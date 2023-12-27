import pandas as pd
import numpy as np
import json
import math
fname=r"ML\model.json"
with open(fname, mode='r', encoding='utf-8') as f:
    datas=json.load(f)
discrete=datas['discrete']
continuous=datas['continuous']
dict0_c=datas['dict0_c']
dict1_c=datas['dict1_c']
dict0_d=datas['dict0_d']
dict1_d=datas['dict1_d']
P0=datas['P0']
P1=datas['P1']
def PreProcess(df):
    df.loc[df['VV']=='低于 0.1','VV']=0
    df['VV']=df['VV'].astype('float64')
    df['Month']=''
    df['Month']=df["Time Stamp"].apply(lambda x:x[3:5])
    df['Month']=df['Month'].astype('int64')
    df['Time']=''
    df['Time']=df["Time Stamp"].apply(lambda x:x[11:13])
    df.drop(columns=["Time Stamp","tR"],inplace=True)
def Predict(df):
    begin=end=0
    size=len(df)
    y=np.zeros(size)
    while begin<size:
        end+=8
        month=str(df.iloc[begin]['Month'])
        sum0,sum1=P0[month],P1[month]
        for i in range(begin,end):
            data=df.iloc[i]
            time=data['Time']
            for attribute in discrete:
                if pd.isna(data[attribute]):
                    continue
                if attribute=='H':
                    continue
                if attribute=='W2':
                    continue
                if data[attribute] in dict0_d[attribute][month][time]:
                    sum0+=dict0_d[attribute][month][time][data[attribute]]
                if data[attribute] in dict1_d[attribute][month][time]:
                    sum1+=dict1_d[attribute][month][time][data[attribute]]
            for attribute in continuous:
                if pd.isna(data[attribute]):
                    continue
                mean,var=dict0_c[attribute][month][time][0],dict0_c[attribute][month][time][1]
                sum0+=-0.5*np.log(2*np.pi*var)-0.5*np.power((data[attribute]-mean),2)/var
                mean,var=dict1_c[attribute][month][time][0],dict1_c[attribute][month][time][1]
                sum1+=-0.5*np.log(2*np.pi*var)-0.5*np.power((data[attribute]-mean),2)/var
        #p=np.power(np.e,sum0)/(np.power(np.e,sum0)+np.power(np.e,sum1))
        p=1-sum0/(sum0+sum1)
        print(p,1-p)
        if p>=0.5:
            y[begin:end]=0
        elif p<=0.5:
            y[begin:end]=1
        else:
            num=math.ceil(p*8)
            y[begin:begin+num]=0
            y[begin+num:end]=1
        begin=end
    return y
""" data_path=r'ML\data.xlsx'
df=pd.read_excel(data_path)
PreProcess(df)
pred=Predict(df) """