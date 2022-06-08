import streamlit as st
import requests
import pandas as pd
from shapely.geometry import Polygon
from shapely.geometry import Point
import geopandas as gpd
import folium
import plotly.express as px
from streamlit_folium import folium_static
import json
import matplotlib.pyplot as plt

with st.echo(code_location="below"):

    st.header("Богатство разных районов Москвы. :money_mouth_face:")

    st.write("""
    Я решил сделать небольшой проект про муниципальные районы Москвы и их различия. Тут будет и недвижимость и тачки и многое другое.
    
    Слева вы можете увидеть меню выбора страницы. Внизу каждой страницы будет код, использованный на ней. 
    Можете спокойно смотреть проект, не беспокоясь о подсчете строк и оценивании, так как в конце я вам сам скажу сколько
    у меня строк и как меня оценивать. :wolf:
    """)

    st.markdown('![](https://github.com/SovBakoid/MyFinalProj/raw/magister/ip-meme.gif)')
