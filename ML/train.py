import pandas as pd
import numpy as np
import collections
import json
#Rainy:0,Not Rainy:1;
def PreProcess(df):
    df.loc[(df['RRR']!='无降水') & (pd.notna(df['RRR'])) & (df['RRR']!='降水迹象'),'RRR']=0
    df.loc[df['RRR']=='无降水','RRR']=1
    df.loc[df['RRR']=='降水迹象','RRR']=1
    df.loc[pd.isna(df['RRR']),'RRR']=1
    df['RRR']=df['RRR'].astype('float64')
    df.loc[df['VV']=='低于 0.1','VV']=0
    df['VV']=df['VV'].astype('float64')
    df["Date"],df['Month']='',''
    df["Date"]=df["Time Stamp"].apply(lambda x:x[0:10])
    df['Month']=df["Time Stamp"].apply(lambda x:x[3:5])
    df['Month']=df['Month'].astype('int64')
    df['Time']=''
    df['Time']=df["Time Stamp"].apply(lambda x:x[11:13])
    df['Year']=''
    df['Year']=df["Time Stamp"].apply(lambda x:x[8:10])
    A=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18']
    B=['18','17','16','15','14','13','12']
    for year in A :
        if year not in B:
            df.drop(df[df['Year']==year].index, inplace=True)
    df.drop(columns=["Time Stamp","tR"],inplace=True)
    df.drop(columns=["Year"],inplace=True)
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
        elif attribute[i]=='Ff':
            continuous.append(attribute[i])
        elif attribute[i]=='Month':
            continue
        elif attribute[i]=='Time':
            continue
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
        dict0[attribute],dict1[attribute]={},{}
        df_new=df.drop(df[pd.isna(df[attribute])].index)
        for month in range(1,13):
            dict0[attribute][month],dict1[attribute][month]={},{}
            for time in ['02','05','08','11','14','17','20','23']:
                df0,df1=df_new.loc[(df['RRR']==0) & (df['Month']==month) & (df['Time']==time)],df_new.loc[(df['RRR']==1) & (df['Time']==time)]
                T0,T1=df0.loc[:,attribute].values.tolist(),df1.loc[:,attribute].values.tolist()
                D0,D1=dict(collections.Counter(T0)),dict(collections.Counter(T1))
                V=list(set(T0+T1))
                len0,len1,len2=len(T0),len(T1),len(V)
                for word in V:
                    n0=D0.get(word,0)
                    n1=D1.get(word,0)
                    D0[word]=np.log((n0+alpha)/(len0+alpha*len2))
                    D1[word]=np.log((n1+alpha)/(len1+alpha*len2))
                dict0[attribute][month][time]=D0
                dict1[attribute][month][time]=D1
    return dict0,dict1
def ContinuousProcess(continuous,df):
    dict0,dict1={},{}
    for attribute in continuous:
        dict0[attribute],dict1[attribute]={},{}
        df_new=df.drop(df[pd.isna(df[attribute])].index)
        for month in range(1,13):
            dict0[attribute][month],dict1[attribute][month]={},{}
            for time in ['02','05','08','11','14','17','20','23']:
                df0,df1=df_new.loc[(df['RRR']==0) & (df['Month']==month) & (df['Time']==time)],df_new.loc[(df['RRR']==1) & (df['Time']==time)]
                T0,T1=df0.loc[:,attribute].values.tolist(),df1.loc[:,attribute].values.tolist()
                list0,list1=[],[]
                list0.extend([np.mean(T0),np.var(T0)])
                list1.extend([np.mean(T1),np.var(T1)])
                dict0[attribute][month][time],dict1[attribute][month][time]=list0,list1
    return dict0,dict1
def PriorPro(df):
    P0,P1={},{}
    for month in range(1,13):
        df0,df1=df.loc[(df['RRR']==0) & (df['Month']==month)],df.loc[(df['RRR']==1) & (df['Month']==month)]
        P0[month],P1[month]=np.log(len(df0)/(len(df0)+len(df1))),np.log(len(df1)/(len(df0)+len(df1)))
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