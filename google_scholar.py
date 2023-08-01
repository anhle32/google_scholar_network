import sys
import pandas as pd
import numpy as np
from scholarly import scholarly
import streamlit as st
import re
import warnings
warnings.filterwarnings("ignore")
from scholar import scraping, models, helpers, scholarNetwork
import networkx as nx
import matplotlib.pyplot as plt




st.title("TIỆN ÍCH GOOGLE SCHOLAR_TRƯỜNG ĐẠI HỌC NGÂN HÀNG TP.HCM")


menu = ["Trích xuất hồ sơ", "Mạng liên kết nghiên cứu"]
choice = st.sidebar.selectbox('Danh mục tính năng', menu)

if choice == 'Trích xuất hồ sơ':    
    st.subheader("TRÍCH XUẤT HỒ SƠ GOOGLE SCHOLAR TÁC GIẢ CỦA TRƯỜNG ĐẠI HỌC NGÂN HÀNG TP.HCM")
    st.image("fig1.png")


    search_query = scholarly.search_author('@hub.edu.vn')
    search_query1= scholarly.search_author('@buh.edu.vn')
    
    list=[]
    for i in search_query:
      list.append(i)
        
    st.title("Danh sách tác giả đang sử dụng mail @hub.edu.vn để đăng ký google scholar")
    data=pd.DataFrame(list)
    data.shape
    st.dataframe(data)
    
    
    
    list1=[]
    for i in search_query1:
      list1.append(i)
    
    st.title("Danh sách tác giả đang sử dụng mail @buh.edu.vn để đăng ký google scholar")
    data1=pd.DataFrame(list1)
    data1.shape
    st.dataframe(data1)
    
    
    df=pd.concat([data,data1])
    
    
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(df)
    
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

elif choice == 'Mạng liên kết nghiên cứu':
    st.subheader("MẠNG LIÊN KẾT NGHIÊN CỨU KHOA HỌC")
    u=st.text_input('Nhập scholar_id')
    if len(u)>0:
        v=st.text_input('Nhập tên tác giả')
        scraping.scrape_single_author(scholar_id=u, scholar_name=v, preferred_browser="chrome")
        g = helpers.build_graph()
        G1=g.edge_rank()
        dt=pd.DataFrame(G1)
        st.dataframe(dt.head(10))
        DG = [(x[0][0], x[0][1], x[1]) for x in G1]
        G = nx.DiGraph()
        G.add_weighted_edges_from(DG)
        fig = plt.figure(figsize=(10, 20),facecolor='white')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        fig1=scholarNetwork.draw_graph(edge_labels.keys(), graph_layout='spring', labels = edge_labels.values())
        st.pyplot(plt.gcf())

