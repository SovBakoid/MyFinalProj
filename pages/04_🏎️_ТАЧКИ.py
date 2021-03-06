import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import sqlite3
import re

with st.echo(code_location="below"):

    st.header("ТАААААЧКИ :tractor:")

    with st.sidebar:
        scrit = st.selectbox("Скрыть основную часть?", ["Нет", "Да"])

    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.write("""Итак, я использовал слитые данные ГИБДД и Яндекс Еда. 
    Сначала нужно было пройтись циклом по куче разных файлов, чтобы их все собрать. 
    Потом я все удалил все персональные данные (почти)))00). Я оставил только файлы, соответсвующие маркам Мерседес и БМВ, потому что иначе не получилось бы в
    гитхаб загрузить, но этого и так хватит.
    Если бы я это делал тут, то сел бы в тюрьму за распространение 
    незаконно полученных перональных данных, а также вам пришлось бы ждать часа четыре. Поэтому смотрите так.""")

    HtmlFile = open('Вывод_данных.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=500, width=1000, scrolling=True)

    HtmlFile = open('Вывод_данных2.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=500, width=1000, scrolling=True)

    st.write("""После я их объединяю по номеру и сразу сохраняю в базу SQL на будущее.""")

    st.write("Теперь запаситесь терпением, потому что ждать вам придется долго, но это того стоит.")

    shurov=pd.read_csv("GBDD_merc_or_bmw.csv").drop(columns='Unnamed: 0')

    god=pd.read_csv("lat_lan_of_vrum_vrum.csv").drop(columns='Unnamed: 0')

    sheesh=shurov.merge(god, how="inner", on='phone_number').drop(columns="gibdd2_car_color")

    sheesh=sheesh.drop_duplicates(keep="first")

    conn=sqlite3.connect("database.sqlite")

    c=conn.cursor()

    #sheesh.to_sql('sheesh', conn) - уже выполнил один раз.

    @st.cache()
    def regions_of_msc_geofra():
        return gpd.read_file("http://gis-lab.info/data/mos-adm/mo.geojson")

    regions_of_msc_geoframe=regions_of_msc_geofra()

    regions_of_msc_geoframe=regions_of_msc_geoframe.drop(columns=["OKATO", "OKTMO",
                                                                  "NAME_AO", "OKATO_AO",
                                                                  "ABBREV_AO", "TYPE_MO"])

    rus_letters=["А", "В", "Е", "К", "М", "Н", "О", "Р", "С", "Т", "У", "Х"]

    if scrit =="Нет":

        sheesh["is_merc"]=sheesh["gibdd2_car_model"].apply(lambda x: 1 if "МЕРСЕДЕС-БЕНЦ" in x else 0)

        sheesh["one"]=sheesh["phone_number"].apply(lambda x: 1)

        sheesh=sheesh.drop(columns="gibdd2_car_model")

        geo_sheesh=gpd.GeoDataFrame(sheesh, geometry=gpd.points_from_xy(sheesh['yandex_longitude'], sheesh['yandex_latitude']))

        geo_sheesh=regions_of_msc_geoframe.sjoin(geo_sheesh, op="intersects", how="inner")

        geo_sheesh2=geo_sheesh.drop(columns=["index_right", "phone_number", "yandex_latitude", "yandex_longitude"]).dissolve(by="NAME", aggfunc='sum')

        geo_sheesh2["merc/bmw"]=geo_sheesh2["is_merc"]/geo_sheesh2["one"]

        st.write("""На карте ниже изображена пропорция мерседесов и бмв. Число 0.6 означает, что от общего
        числа мерсов и бмв мерсы составляют 60%, то есть на каждых двух владельцев бмв в этом районе проживает три владельца мерседеса.
        """)

        geo_sheesh2=geo_sheesh2.reset_index(drop=True)

        fig, ax = plt.subplots(figsize=(15, 12))

        fig=geo_sheesh2.plot(column="merc/bmw", ax=ax, legend=True)

        st.pyplot()

        digits=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        geo_sheesh["cool_count"]=sheesh["phone_number"].apply(lambda x: 0)

        geo_sheesh["gibdd2_car_plate_number"]=geo_sheesh["gibdd2_car_plate_number"].astype("str")

        for i in digits:
            geo_sheesh["cool_count"]=geo_sheesh["cool_count"]+geo_sheesh["gibdd2_car_plate_number"].apply(
                lambda x: 3 if bool(re.match(f'[А-Я]+{i}{i}{i}[А-Я]+\d+', x)) else 0)
            if i!="0":
                geo_sheesh["cool_count"] = geo_sheesh["cool_count"] + geo_sheesh["gibdd2_car_plate_number"].apply(
                    lambda x: 3 if bool(re.match(f'[А-Я]+00{i}[А-Я]+\d+', x)) else 0)
            geo_sheesh["cool_count"] = geo_sheesh["cool_count"] + geo_sheesh["gibdd2_car_plate_number"].apply(
                lambda x: 1 if bool(re.match(f'[А-Я]+[^{i}]{i}{i}[А-Я]+\d+', x)) else 0)
            geo_sheesh["cool_count"] = geo_sheesh["cool_count"] + geo_sheesh["gibdd2_car_plate_number"].apply(
                lambda x: 1 if bool(re.match(f'[А-Я]+{i}[^{i}]{i}[А-Я]+\d+', x)) else 0)
            geo_sheesh["cool_count"] = geo_sheesh["cool_count"] + geo_sheesh["gibdd2_car_plate_number"].apply(
                lambda x: 1 if bool(re.match(f'[А-Я]+{i}{i}[^{i}][А-Я]+\d+', x)) else 0)

        geo_sheesh["cool_count"] = geo_sheesh["cool_count"].fillna(0)

        for i in rus_letters:
            geo_sheesh["cool_count"]=geo_sheesh["cool_count"]+geo_sheesh["gibdd2_car_plate_number"].apply(lambda x: 1 if bool(re.match(f'{i}\d+{i}{i}\d+', x)) else 0)

        geo_sheesh["cool_count"] = geo_sheesh["cool_count"].fillna(0)

        geo_sheesh2=geo_sheesh.drop(columns=["index_right", "phone_number", "yandex_latitude", "yandex_longitude"]).dissolve(by="NAME", aggfunc='sum')

        geo_sheesh2["vtalovost"]=geo_sheesh2["cool_count"]/geo_sheesh2["one"]

        geo_sheesh2=geo_sheesh2.reset_index(drop=True)

        st.write("""Теперь я решил сравнить уровень 'вталовости' номеров. С помощью регулярок я проверял соответствие номера
        машины определенному шаблону и начислял за это баллы. Например, за номер А777АА77 владелец получал 4 балла.
        Далее эти баллы суммировались и делились на общее число владельцев по районам. В итоге картинка получилась такая:
        """)

        fig, ax = plt.subplots(figsize=(15, 12))

        fig=geo_sheesh2.plot(column="vtalovost", ax=ax, legend=True)

        st.pyplot()

    st.write("Теперь вы можете посмотреть на карте, где живут владельцы той или иной модели этих двух марок, но перед этим выберите 'да' на панели слева, иначе вам опять придется ждать вечность.")

    model=st.text_input("Введите любую интересующую модель марки Mercedes или BMW. Попробуйте, например, AMG GLE или X5")

    eng_letters=["A", "B", "E", "K", "M", "H", "O", "P", "C", "T", "Y", "X"]

    for i in range(len(eng_letters)):
        if eng_letters[i] in model:
            model=model.replace(eng_letters[i], rus_letters[i])

    conn.create_function('regexp', 2, lambda x, y: 1 if re.search(x,y) else 0)

    if model!="":

        dicttt={"lat":[], "lon":[]}

        for i in c.execute("SELECT * FROM sheesh WHERE gibdd2_car_model REGEXP ?", [f'.*{model}.*']).fetchall():

            dicttt["lat"].append(i[4])

            dicttt["lon"].append(i[5])

        dfff=pd.DataFrame(dicttt)

        #geo_dfff=gpd.GeoDataFrame(dfff, geometry=gpd.points_from_xy(dfff["lon"], dfff["lat"]))

        m = folium.Map([55.75215, 37.61819], zoom_start=10)

        for ind, row in dfff.iterrows():
            folium.Circle([row.lat, row.lon],
                          radius=10).add_to(m)

        folium_static(m, width=850)

    c.close()

        #geo_dfff=geo_dfff.sjoin(regions_of_msc_geoframe, op="intersects", how="inner")



    #@st.cache()
    #def regions_of_rf_geofra():
        #return gpd.read_file("https://raw.githubusercontent.com/Kreozot/russian-geo-data/master/geo.json")

    #regions_of_rf_geoframe=regions_of_rf_geofra()

    #regions_of_rf_geoframe=regions_of_rf_geoframe.drop(columns=["ID_0", "ISO", "NAME_0", "ID_1", "NL_NAME_1","VARNAME_1","TYPE_1","ENGTYPE_1"])

    #geo_sheesh=gpd.GeoDataFrame(sheesh, geometry=gpd.points_from_xy(sheesh['yandex_longitude'], sheesh['yandex_latitude']))

    #geo_sheesh=regions_of_rf_geoframe.sjoin(geo_sheesh, op="intersects", how="inner")

    #geo_sheesh2=geo_sheesh.dissolve(by="NAME_1", aggfunc='sum')

    #geo_sheesh2["merc/bmw"]=geo_sheesh2["is_merc"]/geo_sheesh2["one"]

    #geo_sheesh2=geo_sheesh2.reset_index(drop=True)

    #fig, ax = plt.subplots(figsize=(12, 17))

    #fig=geo_sheesh2.plot(column="merc/bmw", ax=ax, legend=True)

    #st.pyplot()



