import streamlit as st
from PIL import Image
import pandas as pd
st.title("Chy的第一次深度学习实践大作业")
st.subheader("——对IKUN群体的成分分析")
button1=st.button("项目简介")
if button1:
    st.balloons()
    st.text("1.本项目针对蔡徐坤8月2日发布的微博生日动态，爬取了这条微博的评论，共计五千余条（理论上可达到数万条）。")
    st.text("2.对爬取的评论数据进行分析，绘制了IKUN群体的评论词云图、个人签名词云图。")
    st.text("3.绘制了IKUN群体的IP属地玫瑰图、国内分布热力图（以html形式打开）。")
    st.text("4.注意：本项目仅为学习目的，不含任何人身攻击及不实信息。")
    image1=Image.open("kun.jpg")
    st.image(image1,caption="小黑子禁止入内")
@ st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
df=pd.read_csv("hw2.csv")
csv = convert_df(df)
st.download_button(label="点击下载爬虫数据",data=csv,file_name="hw2.csv",mime='text/csv')
st.text("（注意：不要直接用Excel打开文件，否则是乱码）")
button2=st.button("词云图")
if button2:
    tab1,tab2=st.tabs(["评论词云图","个人签名词云图"])
    with tab1:
        st.image("Figure_1.png",width=800)
    with tab2:
        st.image("Figure_2.png",width=800)
st.text("（点击以下两个按钮下载HTML文件)")
file=open("IP属地比例.html",'r')
button=st.download_button(label="IP属地比例",data=file,file_name="IP属地比例.html",mime='str')
if button:
    st.text("（IKUN遍布全球，甚至在柬埔寨都有分布）")
file=open("IKUN在中国的分布热力图.html",'r')
button=st.download_button(label="IKUN分布热力图",data=file,file_name="热力图.html",mime='str')
if button:
    st.text("可以看到，国内IKUN大多分布在沿海地区")
button3=st.button("总结")
if button3:
    st.subheader("从爬取的五千条热评来看，坤坤的粉丝群体庞大，号召力强，不愧是数一数二的华语顶流👍。")
# Using object notation
add_selectbox = st.sidebar.selectbox(
    "请问你是IKun吗？",
    ("真IKUN", "纯路人", "小黑子")
)
if add_selectbox=="小黑子":
    st.sidebar.text("")
    image1=Image.open("kun1.jpg")
    st.sidebar.image(image1,caption="你就是小黑子？")
elif add_selectbox=="真IKUN":
    st.sidebar.text("鸡你太美")
    image1=Image.open("kun2.webp")
    st.sidebar.image(image1,caption="ctrl")
else:
    st.sidebar.text("纯黑子是吧?")