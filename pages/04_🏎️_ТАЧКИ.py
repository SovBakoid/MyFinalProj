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
import streamlit.components.v1 as components


HtmlFile = open('Вывод_данных.html', 'r', encoding='utf-8')

components.html(HtmlFile.read(), height=1500, width=1300)

