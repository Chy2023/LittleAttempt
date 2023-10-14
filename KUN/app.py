import streamlit as st
from PIL import Image
import pandas as pd
from hw2_module1 import *
from hw2_module2 import *
#Render the file as a web page using streamlit
#Running mode: Enter streamlit run KUN\app.py on the terminal
#Obtain the relevant parameters of microblog comments; The Cookie expires after a period of time and needs to be updated manually
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
         'Cookie':'PC_TOKEN=59cabbbb88; WBStorage=4d96c54e|undefined; XSRF-TOKEN=YJx9XBZCyuoCwJFxm91Vgrkj; login_sid_t=03566ca35ae6f943cd73cd4c61f52fb6; cross_origin_proto=SSL; SUB=_2A25IHQvTDeRhGeFG6FMU-CvLyj6IHXVra3obrDV8PUNbmtANLUelkW9NecUdv1uYwh1bMUAllC2khsLX8oABS1mQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFz63TW03M.ARM0zZ_gaLGB5JpX5KzhUgL.FoMRe02f1h-NeKz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1hepSKnfS02E; ALF=1727704835; SSOLoginState=1696168835; WBPSESS=DlY_SWmwvJp1UZxDBneCv_ke7fxA6M_MywSlrIHS0WsvSA_qFpixWhIFrmcTa9sKb7g6LurcZUDS3eIOAr_fPan-ZoOI4BkjVzN1s1METW4z42PyrpD4jERHQOKpSeD91o4xA2etctBcoji8k36REA==',
         'Referer':'https://weibo.com/1784473157/NlSDGmf4F'}
url="https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4930085347920633&is_show_bulletin=2&is_mix=0&count=10&uid=1776448504&fetch_level=0&locale=zh-CN"
#This function gets 20 comments every 3 seconds, and once called will empty the original data
#So we only need to call it once, and we already have 5000 pieces of data in the database
#GetComment(headers,url)
#Create a heatmap
CreateMap("KUN\hw2.csv","IP")
@ st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
st.title("Chy的第一次深度学习实践大作业")
st.subheader("——对IKUN群体的成分分析")
button1=st.button("项目简介")
add_selectbox = st.sidebar.selectbox(
    "请问你是IKun吗？",
    ("真IKUN", "纯路人", "小黑子")
)
if add_selectbox=="小黑子":
    st.sidebar.text("")
    image1=Image.open("KUN\kun1.jpg")
    st.sidebar.image(image1,caption="你就是小黑子？")
elif add_selectbox=="真IKUN":
    st.sidebar.text("鸡你太美")
    image1=Image.open("KUN\kun2.webp")
    st.sidebar.image(image1,caption="ctrl")
else:
    st.sidebar.text("纯黑子是吧?")
if button1:
    st.balloons()
    st.text("1.本项目针对蔡徐坤8月2日发布的微博生日动态，爬取了这条微博的评论，共计五千余条（理论上可达到数万条）。")
    st.text("2.对爬取的评论数据进行分析，绘制了IKUN群体的评论词云图、个人签名词云图。")
    st.text("3.绘制了IKUN群体的IP属地玫瑰图、国内分布热力图（以html形式打开）。")
    st.text("4.注意：本项目仅为学习目的，不含任何人身攻击及不实信息。")
    image1=Image.open("KUN\kun.jpg")
    st.image(image1,caption="小黑子禁止入内")
button=st.button("预览爬虫数据")
if button:
    df=pd.read_csv("KUN\hw2.csv")
    st.text(df)
    csv = convert_df(df)
    st.download_button(label="点击下载全部数据",data=csv,file_name="hw2.csv",mime='text/csv')
    st.text("（注意：不要直接用Excel打开文件，否则是乱码）")
button2=st.button("词云图")
if button2:
    tab1,tab2=st.tabs(["评论词云图","个人签名词云图"])
    with tab1:
        CreateCloud("KUN\hw2.csv","COMMENT")
    with tab2:
        CreateCloud("KUN\hw2.csv","DESCRIPTION")
button=st.button("IP属地比例")
if button:
    CreatePie("KUN\hw2.csv","IP")
    st.text("（IKUN遍布全球，甚至在柬埔寨都有分布）")
file=open("KUN\IKUN在中国的分布热力图.html",'r')
button=st.download_button(label="IKUN分布热力图",data=file,file_name="热力图.html",mime='str')
if button:
    st.text("可以看到，国内IKUN大多分布在沿海地区")
button3=st.button("总结")
if button3:
    st.subheader("从爬取的五千余条热评来看，坤坤的粉丝群体庞大，号召力强，不愧是数一数二的华语顶流👍。")
url = 'https://github.com/Chy2023/LittleAttempt'
st.markdown(f'''<a href={url}><button style="background-color:GreenYellow;">我的Github仓库</button></a>''',unsafe_allow_html=True)