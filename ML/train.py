import pandas as pd
import numpy as np
import collections
fname=r"ML\training_dataset.xls"
df=pd.read_excel(fname)
discrete,continuous=[],[]
def Overview():
    global df,discrete,continuous
    df.loc[(df['RRR']!='无降水') & (pd.notna(df['RRR'])),'RRR']=1
    df.loc[df['RRR']=='无降水','RRR']=0
    df['RRR']=df['RRR'].astype('float64')
    df.loc[df['VV']=='低于 0.1','VV']=0
    df['VV']=df['VV'].astype('float64')
    df["Date"],df['Time'],df['Rainy']='','',''
    df["Date"]=df["Time Stamp"].apply(lambda x:x[0:10])
    df['Time']=df["Time Stamp"].apply(lambda x:x[11:16])
    df.drop(columns=["Time Stamp"],inplace=True)
    list1=set(df.loc[:,'Date'].values.tolist())
    for item in list1:
        list2=df.loc[df['Date']==item,'RRR'].values.tolist()
        if 1 in list2:
            df.loc[df['Date']==item,'Rainy']=1
        elif np.isnan(list2).sum()==len(list2):
            df.loc[df['Date']==item,'Rainy']=np.nan
        else:
            df.loc[df['Date']==item,'Rainy']=0
    df.drop(df[pd.isna(df['Rainy'])].index, inplace=True)
    attribute=df.columns.values
    drop=[]
    list=df.notnull().mean()
    for i in range(0,len(list)):
        if list.iloc[i]<0.2:
            drop.append(attribute[i])
        elif df.iloc[:,i].dtype=='object':
            discrete.append(attribute[i])
        elif df.iloc[:,i].dtype=='int64':
            discrete.append(attribute[i])
        elif attribute[i]=='tR':
            discrete.append(attribute[i])
        elif attribute[i]=='RRR':
            discrete.append(attribute[i])
        else:
            continuous.append(attribute[i])
    df.drop(drop,axis=1,inplace=True)
    discrete.remove('Rainy')
Overview()
def DiscreteProcess():
    global discrete,df
    dict0,dict1={},{}
    for attribute in discrete:
        df_new=df.drop(df[pd.isna(df[attribute])].index)
        df0,df1=df_new.loc[df['Rainy']==0],df_new.loc[df['Rainy']==1]
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
            D0[word]=np.log((n0+1)/(len0+len2))
            D1[word]=np.log((n1+1)/(len1+len2))
        dict0[attribute]=D0
        dict1[attribute]=D1
    return dict0,dict1
def ContinuousProcess():
    global continuous,df
    dict0,dict1={},{}
    for attribute in continuous:
        df_new=df.drop(df[pd.isna(df[attribute])].index)
        df0,df1=df_new.loc[df['Rainy']==0],df_new.loc[df['Rainy']==1]
        T0,T1=df0.loc[:,attribute].values.tolist(),df1.loc[:,attribute].values.tolist()
        list0,list1=[],[]
        list0.append(np.mean(T0))
        list0.append(np.var(T0))
        list1.append(np.mean(T1))
        list1.append(np.var(T1))
        dict0[attribute],dict1[attribute]=list0,list1
    return dict0,dict1
def PriorPro():
    global df
    df0,df1=df.loc[df['Rainy']==0],df.loc[df['Rainy']==1]
    P0,P1=len(df0)/len(df),len(df1)/len(df)
    return P0,P1
dict0_c,dict1_c=ContinuousProcess()
dict0_d,dict1_d=DiscreteProcess()
P0,P1=PriorPro()
tp=tn=fp=fn=0
for i in range(0,len(df)):
    data=df.iloc[i]
    sum0,sum1=np.log(P0),np.log(P1)
    if(data['Rainy']==0):
        label=0
    else:
        label=1
    for attribute in discrete:
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
    if (sum0>=sum1 and label==0):
        tn+=1
    elif (sum0>=sum1 and label==1):
        fn+=1
    elif (sum0<=sum1 and label==1):
        tp+=1
    else:
        fp+=1
print("Accuracy={}".format((tp+tn)/(tp+tn+fn+fp)))
print("Precision={}".format(tp/(tp+fp)))
print("Recall={}".format(tp/(tp+fn)))
print("F-score={}".format(2/(2+(fn+fp)/tp)))
""" print(discrete)
print(continuous)
print(dict0_c)
print(dict1_c)
for attribute in discrete:
    if attribute=='Date':
        continue
    print(dict0_d[attribute])
for attribute in discrete:
    if attribute=='Date':
        continue
    print(dict1_d[attribute])    """ 
#高斯贝叶斯+多项式贝叶斯分类器
#数据完整度不足20%的舍去。9：(8,9,15,18,19,24,25,26,27)
#贝叶斯分类器忽略了缺失的数据，平滑系数alpha
#SVC?
#标签缺失2/3?
#其余缺失的数据：若是离散数据，则用众数代替；若是连续数据，则用平均数代替?
#Time Stamp处理
#attribute有待进一步观察