import streamlit as st
import requests
import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import json
import matplotlib.pyplot as plt
import numpy as np

with st.echo(code_location="below"):

    cookies = {
        'cf_clearance': 'Z3LHiJ7VZ4ksm5gXR0Ndh7lXgMI2TNlaAqzyTPMuBdY-1653477997-0-150',
        '_CIAN_GK': 'f4f4b97d-21e5-4d86-86fe-84e26fa9d09e',
        'session_region_id': '1',
        'login_mro_popup': '1',
        '_ga': 'GA1.2.155874544.1653478003',
        'uxfb_usertype': 'searcher',
        'tmr_lvid': '8dad91d7b6c627d219607c509d212985',
        'tmr_lvidTS': '1649167264680',
        '_ym_uid': '1649167265941174706',
        '_ym_d': '1653478003',
        'afUserId': '94fcfaa2-df14-46ed-9936-5cdc78185940-p',
        'adrcid': 'AKUGW_ilc69pXCacE44IbAQ',
        'cookie_agreement_accepted': '1',
        '_gcl_au': '1.1.1014650449.1653478461',
        'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
        'sopr_session': '1786c0b4427b4571',
        '_gid': 'GA1.2.1915935594.1654429072',
        '_ym_visorc': 'b',
        '_ym_isad': '2',
        '_cc_id': '3fffa5b61d7d9b8d0c576b20f966fe7e',
        'panoramaId_expiry': '1655033880098',
        'panoramaId': 'e63664efb33c6390a7da520d8f7616d5393829db752e9b30d90a017a87ee1902',
        'AF_SYNC': '1654429210991',
        'uxs_uid': 'f4a10900-e4c4-11ec-b65c-752149a6cbfc',
        '_hjSessionUser_2021803': 'eyJpZCI6IjA5NDRjMDc3LTQ5MWUtNTFjZS04ZDJlLTQxNTA2MjBkYmQwMyIsImNyZWF0ZWQiOjE2NTQ0Mjk1MTIwNjQsImV4aXN0aW5nIjp0cnVlfQ==',
        'session_main_town_region_id': '1',
        'serp_registration_trigger_popup': '1',
        'do_not_show_mortgage_banner': '1',
        '__cf_bm': 'lbQ8q0OCIJ.tqI9ttV3_3BbH9pFbytCiPstMv3QwDQY-1654432249-0-AWz5XRxbPY1/NzI8ClZNMmH4F1MQF0vRPK5laJStETc+rEtDxlXtRhTwZyXmdbIpl67WmsW/mBI96gwu30hRaZQ=',
        'tmr_reqNum': '136',
    }

    headers = {
        'authority': 'api.cian.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'text/plain;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'cf_clearance=Z3LHiJ7VZ4ksm5gXR0Ndh7lXgMI2TNlaAqzyTPMuBdY-1653477997-0-150; _CIAN_GK=f4f4b97d-21e5-4d86-86fe-84e26fa9d09e; session_region_id=1; login_mro_popup=1; _ga=GA1.2.155874544.1653478003; uxfb_usertype=searcher; tmr_lvid=8dad91d7b6c627d219607c509d212985; tmr_lvidTS=1649167264680; _ym_uid=1649167265941174706; _ym_d=1653478003; afUserId=94fcfaa2-df14-46ed-9936-5cdc78185940-p; adrcid=AKUGW_ilc69pXCacE44IbAQ; cookie_agreement_accepted=1; _gcl_au=1.1.1014650449.1653478461; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; sopr_session=1786c0b4427b4571; _gid=GA1.2.1915935594.1654429072; _ym_visorc=b; _ym_isad=2; _cc_id=3fffa5b61d7d9b8d0c576b20f966fe7e; panoramaId_expiry=1655033880098; panoramaId=e63664efb33c6390a7da520d8f7616d5393829db752e9b30d90a017a87ee1902; AF_SYNC=1654429210991; uxs_uid=f4a10900-e4c4-11ec-b65c-752149a6cbfc; _hjSessionUser_2021803=eyJpZCI6IjA5NDRjMDc3LTQ5MWUtNTFjZS04ZDJlLTQxNTA2MjBkYmQwMyIsImNyZWF0ZWQiOjE2NTQ0Mjk1MTIwNjQsImV4aXN0aW5nIjp0cnVlfQ==; session_main_town_region_id=1; serp_registration_trigger_popup=1; do_not_show_mortgage_banner=1; __cf_bm=lbQ8q0OCIJ.tqI9ttV3_3BbH9pFbytCiPstMv3QwDQY-1654432249-0-AWz5XRxbPY1/NzI8ClZNMmH4F1MQF0vRPK5laJStETc+rEtDxlXtRhTwZyXmdbIpl67WmsW/mBI96gwu30hRaZQ=; tmr_reqNum=136',
        'origin': 'https://www.cian.ru',
        'referer': 'https://www.cian.ru/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    }

    proxy={'http': "http://93.123.226.23:81",
           'https': "http://91.199.223.214:3128"}

    data = '{"zoom":15,"bbox":[{"bottomRight":{"lat":55.542748557514244,"lng":37.923427700607334},"topLeft":{"lat":55.92313314646403,"lng":37.22287762126163}}],"jsonQuery":{"region":{"type":"terms","value":[1]},"_type":"flatsale","engine_version":{"type":"term","value":2}},"extended":true,"subdomain":"www"}'

    url='https://api.cian.ru/search-offers-map/v1/get-clusters-for-map/'

    @st.cache()
    def cian_sosat():
        return (requests.post(url, cookies=cookies, headers=headers, data=data))

    helloaboba=cian_sosat()

    #with open('helloaboba', 'wb') as f: - в локальной версии тут не стоят решетки
        #f.write(helloaboba.content) - зашеренный стримлит просто не может так жестко парсить данные из-за открытого IP и прокси не помогают.

    with open('helloaboba', 'rb') as f:
        helloaboba=f.read()

    yyyuuu= json.loads(helloaboba.decode("utf-8"))

    ya_uedu_zhit_v_abakan={"weight":[], "lat": [], "lon":[], "minprice":[], "maxprice":[]}

    for yyy in yyyuuu['filtered']:
        ya_uedu_zhit_v_abakan["lat"].append(yyy['coordinates']['lat'])
        ya_uedu_zhit_v_abakan["lon"].append(yyy['coordinates']['lng'])
        ya_uedu_zhit_v_abakan["weight"].append(yyy['count'])
        ya_uedu_zhit_v_abakan["minprice"].append(yyy['minPrice'])
        ya_uedu_zhit_v_abakan["maxprice"].append(yyy['maxPrice'])

    ya_uedu_zhit_v_abakan_frame=pd.DataFrame(ya_uedu_zhit_v_abakan)

    ya_uedu_zhit_v_abakan_frame["avgprice"]=(ya_uedu_zhit_v_abakan_frame["minprice"]+ya_uedu_zhit_v_abakan_frame["maxprice"])/2

    abakan_gdf = gpd.GeoDataFrame(ya_uedu_zhit_v_abakan_frame, geometry = gpd.points_from_xy(ya_uedu_zhit_v_abakan_frame['lon'], ya_uedu_zhit_v_abakan_frame['lat']))

    @st.cache()
    def moskva():
        with open('Inside_mkAD.geojson', encoding='utf-8') as mmmomom:
            return(json.load(mmmomom))

    vnutri_mkada=moskva()

    vnutri_mkada_poly = Polygon(vnutri_mkada['features'][0]['geometry']['coordinates'][0])

    center_df=pd.DataFrame({"name":"Москва", "poly":vnutri_mkada_poly}, index=[0])

    center_gdf=gpd.GeoDataFrame(center_df, geometry = 'poly')

    abakan_inside_mkad=abakan_gdf.sjoin(center_gdf, op="intersects", how="inner").reset_index(drop=True).drop(columns="index_right")

    m = folium.Map([55.75215, 37.61819], zoom_start=11)

    for ind, row in abakan_inside_mkad.iterrows():
        folium.Circle([row.lat, row.lon],
                      radius=10).add_to(m)

    folium_static(m, width=850)

    @st.cache()
    def regions_of_msc_geofra():
        return gpd.read_file("http://gis-lab.info/data/mos-adm/mo.geojson")

    regions_of_msc_geoframe=regions_of_msc_geofra()

    regions_of_msc_geoframe=regions_of_msc_geoframe.drop(145)

    regions_of_msc_geoframe_inside_moscow=regions_of_msc_geoframe.sjoin(center_gdf, op="intersects", how="inner").drop(columns=["index_right","name"])

    regions_with_prices=regions_of_msc_geoframe_inside_moscow.sjoin(abakan_inside_mkad)

    regions_with_prices["price_x_weight"]=regions_with_prices["avgprice"]*regions_with_prices["weight"]

    regions_avg_prices2=regions_with_prices.dissolve(by="NAME", aggfunc='sum')

    regions_avg_prices2["real_avg_price"]=regions_avg_prices2["price_x_weight"]/regions_avg_prices2["weight"]

    regions_avg_prices2=regions_avg_prices2.drop(columns=["price_x_weight", "avgprice", "minprice", "maxprice", 'lat', "lon"])

    regions_avg_prices2=regions_avg_prices2.reset_index()

    st.set_option('deprecation.showPyplotGlobalUse', False)

    fig, ax = plt.subplots(figsize=(12, 12))

    fig=regions_avg_prices2.plot(column="real_avg_price", ax=ax, legend=True)

    st.pyplot()

    #georegions_of_msc=gpd.GeoDataFrame(regions_of_msc, geometry = [Polygon([[[p.x, p.y] for p in f1] for f1 in [[Point(i[0], i[1]) for i in row["cords"]] for _, row in regions_of_msc.iterrows()]])])

    regions_avg_prices2["ln_avg"]=np.log(regions_avg_prices2["real_avg_price"])

    fig, ax = plt.subplots(figsize=(12, 12))

    fig = regions_avg_prices2.plot(column="ln_avg", ax=ax, legend=True)

    st.pyplot()