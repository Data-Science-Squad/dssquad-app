#Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from datetime import date, timedelta
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image

#Setting Page layout
st.set_page_config(layout="wide")

#Importing the dataset
df = pd.read_csv('E:/DS_squad/crime_weekdates.csv')

#Datatype conversions
df['just_date'] = pd.to_datetime(df['just_date']).dt.date
df['Police_district'] = df['Police_district'].astype('string')

#Feature Engineering
a = []
for i in df.no_of_crimes:
    if i>30:
        a.append('Crime >= 30')
    else:
        a.append('Crime < 30')
df['Days_with_much_crime'] = a
df['Days_with_much_crime'] = df['Days_with_much_crime'].astype('string')

#Logo and Headline
image = Image.open('E:/DS_squad/logo_new.png')
col5,col6 = st.beta_columns([4,70])
col5.image(image,channels= 'BGR', use_column_width='auto')
col6.markdown("<h2 style='text-align: left; color: black;'>Buffalo Police Department, N.Y.</h2>", unsafe_allow_html=True)

#Setting layout for each plots
col1,col2 = st.beta_columns(2)
col3,col4 = st.beta_columns([1,0.8])

#Plot : 1
def plotly_map():
    start_date = col1.selectbox('Select Week date of Crime', (df['just_date'].unique()))
    px.set_mapbox_access_token(open("E:/DS_squad/new.mapbox_token").read())
    a = df.loc[df.just_date == start_date, :]
    fig = px.scatter_mapbox(a,lat=a['latitude'],
                            lon=a['longitude'],
                            color= a['no_of_crimes'],
                            size = a['no_of_crimes'],
                            hover_name = a['Police_district'],
                            size_max=35,
                            color_continuous_scale= px.colors.sequential.Emrld,
                            width= 500,
                            height= 505
                            )
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom= 9,
        title={
            'text': "Map",
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig

#Plot : 2
def plotly_line():
    #global police_districts_dropdown
    police_districts_dropdown = col2.multiselect('Select Police District(s)',
                                                 ['District A', 'District B', 'District C', 'District D', 'District E'])
    fig = px.scatter(df, x='just_date', y='no_of_crimes', color=df['Police_district'],height= 500,width=760)
    df1 = df[df['Police_district'].isin(police_districts_dropdown)]
    if len(df1) != 0:
        fig = px.scatter(df1, x='just_date', y='no_of_crimes', color=df1['Police_district'],height= 500,width=760)
    fig.update_traces(mode = 'lines+markers')
    fig.update_layout(
        title={
            'text': "Forecasting trend for the next 4 weeks",
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig

#Plot : 3
def plotly_bar():
    fig = px.bar(df,x= 'Police_district', y = 'no_of_crimes', color= 'Days_with_much_crime', hover_name= 'just_date', width= 726,height= 440)
    fig.update_layout(
        title={
            'text': "Crimes with respect to Police Districts and Dates",
            'y': 1,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig

#Plot : 4
def dataframe():
    df2 = df.loc[:,['just_date','Police_district','no_of_crimes']]
    col4.markdown("<p style='text-align: center; color: black;'>Table of crime forecasts</p>", unsafe_allow_html=True)
    col4.write('\n')
    return col4.dataframe(df2, width=565, height=303)


#Function calls
col1.plotly_chart(plotly_map(),use_container_width=True)
col2.plotly_chart(plotly_line())
col3.plotly_chart(plotly_bar())
dataframe()