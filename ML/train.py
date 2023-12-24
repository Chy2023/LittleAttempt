import pandas as pd
import numpy as np
import collections
import json
#Rainy:0,Not Rainy:1;
def PreProcess(df):
    df.loc[(df['RRR']!='无降水') & (pd.notna(df['RRR'])),'RRR']=0
    df.loc[df['RRR']=='无降水','RRR']=1
    df['RRR']=df['RRR'].astype('float64')
    df.loc[df['VV']=='低于 0.1','VV']=0
    df['VV']=df['VV'].astype('float64')
    df["Date"],df['Month']='',''
    df["Date"]=df["Time Stamp"].apply(lambda x:x[0:10])
    df['Month']=df["Time Stamp"].apply(lambda x:x[3:5])
    df.drop(columns=["Time Stamp","tR"],inplace=True)
def AddLabel(df):
    list=dict(df['Date'].value_counts(sort=False)).values()
    index=df.columns.get_loc('RRR')
    begin=end=0
    for num in list:
        end+=num
        list1=df.iloc[begin:end]['RRR'].values.tolist()
        if 0 in list1:
            df.iloc[begin:end,index]=0
        elif np.isnan(list1).sum()==0 and len(list1)==8:
            df.iloc[begin:end,index]=1
        else:
            df.iloc[begin:end,index]=np.nan
        begin=end
    df.drop(df[pd.isna(df['RRR'])].index, inplace=True)
    df.drop(columns=["Date"],inplace=True)
def TagSort(df):
    drop,discrete,continuous=[],[],[]
    attribute=df.columns.values
    list=df.notnull().mean()
    for i in range(0,len(list)):
        if list.iloc[i]<0.2:
            drop.append(attribute[i])
        elif attribute[i] in ['N','Nh','Cm']:
            drop.append(attribute[i])
        elif df.iloc[:,i].dtype=='object':
            discrete.append(attribute[i])
        elif df.iloc[:,i].dtype=='int64':
            discrete.append(attribute[i])
        elif attribute[i]=='RRR':
            continue
        else:
            continuous.append(attribute[i])
    df.drop(drop,axis=1,inplace=True)
    return discrete,continuous
def DiscreteProcess(alpha,df,discrete):
    dict0,dict1={},{}
    for attribute in discrete:
        df_new=df.drop(df[pd.isna(df[attribute])].index)
        df0,df1=df_new.loc[df['RRR']==0],df_new.loc[df['RRR']==1]
        T0,T1=df0.loc[:,attribute].values.tolist(),df1.loc[:,attribute].values.tolist()
        D0,D1=dict(collections.Counter(T0)),dict(collections.Counter(T1))
        V=list(set(T0+T1))
        len0,len1,len2=len(T0),len(T1),len(V)
        for word in V:
            if word in D0:
                n0=D0[word]
            else:
                n0=0
            if word in D1:
                n1=D1[word]
            else:
                n1=0
            D0[word]=np.log((n0+alpha)/(len0+alpha*len2))
            D1[word]=np.log((n1+alpha)/(len1+alpha*len2))
        dict0[attribute]=D0
        dict1[attribute]=D1
    return dict0,dict1
def ContinuousProcess(continuous,df):
    dict0,dict1={},{}
    for attribute in continuous:
        df_new=df.drop(df[pd.isna(df[attribute])].index)
        df0,df1=df_new.loc[df['RRR']==0],df_new.loc[df['RRR']==1]
        T0,T1=df0.loc[:,attribute].values.tolist(),df1.loc[:,attribute].values.tolist()
        list0,list1=[],[]
        list0.extend([np.mean(T0),np.var(T0)])
        list1.extend([np.mean(T1),np.var(T1)])
        dict0[attribute],dict1[attribute]=list0,list1
    return dict0,dict1
def PriorPro(df):
    df0,df1=df.loc[df['RRR']==0],df.loc[df['RRR']==1]
    P0,P1=len(df0)/len(df),len(df1)/len(df)
    return P0,P1
fname=r"ML\training_dataset.xls"
df=pd.read_excel(fname)
PreProcess(df)
AddLabel(df)
discrete,continuous=TagSort(df)
dict0_c,dict1_c=ContinuousProcess(continuous,df)
dict0_d,dict1_d=DiscreteProcess(1e-10,df,discrete)
P0,P1=PriorPro(df)
fname=r"ML\model.json"
with open(fname,mode='w',encoding='utf-8') as f:
    datas={'discrete':discrete,'continuous':continuous,'dict0_c':dict0_c,'dict1_c':dict1_c,'dict0_d':dict0_d,'dict1_d':dict1_d,'P0':P0,'P1':P1}
    json.dump(datas, f)