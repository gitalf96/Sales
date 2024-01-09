import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.express as px 
import streamlit as st 
from streamlit_option_menu import option_menu 
import altair as alt

## background: url("https://img.freepik.com/free-photo/solid-concrete-wall-textured-backdrop_53876-129493.jpg?w=740&t=st=1704454131~exp=1704454731~hmac=d6bbd0f53bbd31f572eb17868195e78038904cc9d47544dbe5f7a59cec97b68b");

st.set_page_config(page_title="Sales Dashboard",page_icon='bar-chart',layout='wide')
st.title(':red[Automobile Sales Dashboard]')

st.markdown(
    """
    <style>
    div[data-testid="stApp"]  {
        background-color: rgba(0,0,0, 0.9);
            }
   </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-colour: rgbat(238,232,170,0.8);
    color: white;
}
</style>
""",
    unsafe_allow_html=True
)
st.markdown("""
<style>
div[data-testid="column"] {
   background-color: rgba(255,255,0, 0.6);
   border: 3px solid rgba(218,165,32,0.9);
   padding: 5% 2% 7% 1%;
   border-radius:7px;
   color: rgb((255,0,0));
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="element-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: black;
}
</style>
"""
, unsafe_allow_html=True)

df=pd.read_csv('Auto Sales data.csv')
# df.head()
# df.shape
# df.info()
# df['MSRP'].describe()
df.isnull().sum()


# print(round(v))


with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options=["KPI and Tables","Charts"],
        icons=["table","bar-chart"],
        menu_icon="cast",
        default_index=0,
    )

with st.sidebar:
  product_filter = st.selectbox("Select Product", pd.unique(df['PRODUCTLINE']))
  Year_filter = st.selectbox("Select Year", pd.unique(df['Year']))
#   Country_filter = st.selectbox("Select Country", pd.unique(df['COUNTRY']))
  
placeholder = st.empty()

df = df[df["PRODUCTLINE"] == product_filter]
df = df[df["Year"] == Year_filter]
# df = df[df["COUNTRY"]== Country_filter]

if selected=="KPI and Tables":

    with placeholder.container():
        col1,col2=st.columns(2)
        col1.metric(label="Sales for each product",
               value=sum(df.SALES))
        col2.metric(label="No. of Product",
                    value=df.ORDERNUMBER.count())
        
        st.subheader(":green[Sales from Each Quarter]")

        a=df.query("Month==['Jan','Feb','Mar']")["SALES"].sum()
        b=df.query("Month==['Apr','May','Jun']")["SALES"].sum()
        c=df.query("Month==['Jul','Aug','Sep']")["SALES"].sum()
        d=df.query("Month==['Oct','Nov','Dec']")["SALES"].sum()

        col1,col2,col3,col4 = st.columns(4)
        col1.metric(label="First Quarter",
        value=round(a))
        col2.metric(label="Second Quarter",
                value=round(b))
        col3.metric(label="Third Quarter",
        value=round(c))
        col4.metric(label="Fourth Quarter",
                value=round(d))
       


if selected=="Charts":
    

    c1,c2=st.tabs(["No.of Orders in Under Each Category","Sales in"])

    chart = alt.Chart(df).mark_bar().encode(
        x='DEALSIZE',
        y='count(ORDERNUMBER)',
        # color='Type',
        ).interactive()
        
    with c1:
            st.altair_chart(chart, theme="streamlit", use_container_width=True)

    bart = alt.Chart(df,title="Sales Trend across the months" ).mark_line().encode(
        x='Month',
        y='sum(SALES)',
        ).interactive()
        
    (bart).configure_title(fontSize=14).configure(background='#FF0000')
    with c2:
            st.altair_chart(bart,theme=None, use_container_width=True)


        



