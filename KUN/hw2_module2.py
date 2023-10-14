import numpy as np
import pandas as pd
import streamlit_echarts as ste
import streamlit as st
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from PIL import Image
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.charts import Pie
from pyecharts.globals import CurrentConfig
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/assets/"
def CreateCloud(filename,tag):
    df=pd.read_csv(filename)
    text="".join(str(i) for i in df[tag].tolist())
    words=jieba.cut(text)
    word_counts=Counter(words)
    img=Image.open("KUN\leaf.png")
    img_array=np.array(img)
    wc=WordCloud(width=1000, height=800, background_color="white", max_words=200,mask=img_array,font_path="STXINGKA.TTF")
    wc.generate_from_frequencies(word_counts)
    #Use the matplotlib library to visualize the word cloud map
    figure=plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(figure)
def CreateMap(filename,tag):
    df = pd.read_csv(filename, encoding='utf-8')[tag]
    data = df.value_counts()
    datas = [(i, int(j)) for i, j in zip(data.index, data.values)]
    #print(datas)
    geo = (Geo(init_opts=opts.InitOpts(width='1200px', height='550px', theme='dark'),is_ignore_nonexistent_coord=True)
    .add_schema(maptype="china")                       #maptype
    .add(series_name="评论数量",      #Series name
         data_pair=datas,          #Data item (coordinate point name, coordinate point value)
         blur_size=10,
         symbol_size= 12,
         point_size=20,
         #type_=ChartType.HEATMAP  #Type is selected as heat map
         type_= "heatmap",
        )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=300,is_piecewise=True),
        title_opts=opts.TitleOpts(title="IKUN在中国的分布热力图"))
    )
    #It is displayed as an HTML file
    geo.render( 'KUN\IKUN在中国的分布热力图.html')
def CreatePie(filename,tag):
    f = pd.read_csv(filename, encoding='utf-8')[tag]
    data = f.value_counts()
    #datas = [(i, int(j)) for i, j in zip(data.index, data.values)]
    #print(datas)
    provinces=[i for i, j in zip(data.index, data.values)]
    num = [int(j) for i, j in zip(data.index, data.values)]
    color_series = ['#FAE927','#E9E416','#C9DA36','#9ECB3C','#6DBC49',
                '#37B44E','#3DBA78','#14ADCF','#209AC9','#1E91CA',
                '#2C6BA0','#2B55A1','#2D3D8E','#44388E','#6A368B'
                '#7D3990','#A63F98','#C31C88','#D52178','#D5225B',
                '#D02C2A','#D44C2D','#F57A34','#FA8F2F','#D99D21',
                '#CF7B25','#CF7B25','#CF7B25']
    #Create a DataFrame
    df = pd.DataFrame({'provinces': provinces, 'num': num})
    #Extract data
    v = df['provinces'].values.tolist()
    d = df['num'].values.tolist()
    pie1 = Pie(init_opts=opts.InitOpts(width='1400px', height='800px'))
    #Set color
    pie1.set_colors(color_series)
    pie1.add("", [list(z) for z in zip(v, d)],
        radius=["30%", "100%"],
        center=["50%", "50%"],
        rosetype="area"
    )
#Set global configuration items
    pie1.set_global_opts(title_opts=opts.TitleOpts(title='IKUN分布图',
                                               title_textstyle_opts=opts.TextStyleOpts(font_size=25,color= '#0085c3'),
                                               subtitle_textstyle_opts= opts.TextStyleOpts(font_size=50,color= '#003399'),
                                               pos_right= 'center',pos_left= 'center',pos_top='42%',pos_bottom='center'
                                              ),
                     legend_opts=opts.LegendOpts(is_show=False),
                     toolbox_opts=opts.ToolboxOpts())
#Set series of configuration items
    pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                               formatter="{b}:{c}人", font_style="italic",
                                               font_weight="bold", font_family="SimHei"
                                               ),
                     )
    ste.st_pyecharts(pie1)