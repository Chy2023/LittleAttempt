import pandas as pd
import numpy as np
import json
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
    df.drop(columns=["Time Stamp","tR"],inplace=True)
def Predict(df):
    begin=end=0
    size=len(df)
    y=np.zeros(size)
    while begin<size:
        end+=8
        sum0,sum1=np.log(P0),np.log(P1)
        for i in range(begin,end):
            data=df.iloc[i]
            for attribute in discrete:
                if pd.isna(data[attribute]):
                    continue
                if data[attribute] in dict0_d[attribute]:
                    sum0+=dict0_d[attribute][data[attribute]]
                if data[attribute] in dict1_d[attribute]:
                    sum1+=dict1_d[attribute][data[attribute]]
            for attribute in continuous:
                if pd.isna(data[attribute]):
                    continue
                mean,var=dict0_c[attribute][0],dict0_c[attribute][1]
                sum0+=-0.5*np.log(2*np.pi*var)-0.5*np.power((data[attribute]-mean),2)/var
                mean,var=dict1_c[attribute][0],dict1_c[attribute][1]
                sum1+=-0.5*np.log(2*np.pi*var)-0.5*np.power((data[attribute]-mean),2)/var
        if sum0>=sum1:
            y[begin:end]=0
        else:
            y[begin:end]=1
        begin=end
    return y