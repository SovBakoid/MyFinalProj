import streamlit as st
import pandas as pd
import scrapy
import networkx as nx
from itertools import combinations
from pyvis.network import Network
import streamlit.components.v1 as components

with st.echo(code_location='below'):

    st.header("Знаменитости, паук и сеть. :spider: :spider_web:")

    st.write("""Я написал паучка Scrapy, который ходил по вот этому сайту https://www.bankgorodov.ru/region/moskva/famous/1, сохранял личные ссылки, 
    листал подборку, заходил на страницу каждого человека из подборки и сохранял все ссылки на любых других людей. Код паучка смотрите внизу.""")

    class FameSpider(scrapy.Spider):
        name = 'famousspider'
        start_urls = ['https://www.bankgorodov.ru/region/moskva/famous/1']

        def parse2(self, response):
            titleolol=response.css("h1.box-title::text").get()
            for link in response.css(".desc-text a"):
                yield {"first": titleolol, "second": link.attrib['href']}

        def parse1(self, response):
            for celebrity in response.css("li.celebrity"):
                m = 'https://www.bankgorodov.ru' + str(celebrity.css('a.h-link').attrib['href'])
                yield {"first": celebrity.css('a.h-link::text').get(),
                       "second": m}
                yield response.follow(m, self.parse2)

        def parse(self, response):
            for celebrity in response.css("li.celebrity"):
                m = 'https://www.bankgorodov.ru' + str(celebrity.css('a.h-link').attrib['href'])
                yield {"first": celebrity.css('a.h-link::text').get(),
                       "second": m}
                yield response.follow(m, self.parse2)

            for i in range(2, 22):
                new_url='https://www.bankgorodov.ru/region/moskva/famous/' + str(i)
                yield response.follow(new_url, self.parse1)

        #scrapy runspider /Users/XXX/PycharmProjects/pythonProject1/pages/spider.py -O table.csv

    fp_n_l=pd.read_csv("table.csv")

    hello_mf=[]

    for _, row in fp_n_l.iterrows():
        if "http" in row["second"]:
            hello_mf.append(row["second"])
        else:
            hello_mf.append("https://www.bankgorodov.ru" + row["second"])

    fp_n_l["second"]=pd.Series(hello_mf)

    fp_n_l=fp_n_l[fp_n_l["second"]!= "https://www.bankgorodov.ru/"]

    fp_n_l=fp_n_l[fp_n_l["second"].str.contains("famous-person")]

    st.write("Починив вид части ссылок и убрав все лишние, то есть все, которые не ведут на других известных людей я получил вот такой датафрэм.")

    fp_n_l

    all_people=fp_n_l["first"].unique().tolist()

    fp2=fp_n_l.groupby('second')['first'].apply(lambda x : list(combinations(x.values,2))).apply(pd.Series).stack().reset_index(level=0,name='first')

    fp2["p1"]=pd.Series([row["first"][0] for _, row in fp2.iterrows()])

    fp2["p2"]=pd.Series([row["first"][1] for _, row in fp2.iterrows()])

    fp2=fp2.drop(columns=["second","first"])

    fp2=fp2[fp2["p1"]!=fp2["p2"]]

    fp2=fp2.drop_duplicates(keep='first')

    st.write("Если у кого-то была ссылка на другого человека, то я их связывал друг с другом. После очистки датафрэйма от дубликатов и ссылок на самого себя получилось вот это.")

    fp2

    st.write("Получается, что этот датафрэйм показывает все взаимные упоминания на личных страничках. Я создал точки, соответсвующие каждому известному москвичу, перечисленному на сайте, и связал их по признаку наличия каких-то взаимотоношений")

    st.write("Подождите немного когда это все загрузится и вы сами все увидите.")

    st.write("Присмотритесь, графы движутся!! А еще вы можете двигать их сами!")

    lonly_bois=c = [x for x in all_people if x not in fp2["p1"].unique().tolist()]

    moscow_graphs=nx.DiGraph([(row["p1"], row["p2"]) for _, row in fp2.iterrows()])

    moscow_graphs.add_nodes_from(tuple(lonly_bois))

    nt = Network('900px', '900px', bgcolor='#222222', font_color='white')

    nt.from_nx(moscow_graphs)

    nt.repulsion(node_distance=420, central_gravity=0.33,
                           spring_length=110, spring_strength=0.10,
                           damping=0.95)

    nt.show('nx.html')

    HtmlFile = open('nx.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=1000, width=1000)

    st.balloons()

    st.write("Теперь вы можете выбрать любого интересующего вас известного москвича и посмотреть с кем он связан.")

    perosn=st.selectbox('Кого вы хотите выбрать?', fp2["p1"].unique().tolist())

    sub=moscow_graphs.subgraph([perosn]+list(moscow_graphs.neighbors(perosn)))

    net = Network('500px', '500px', bgcolor='#222222', font_color='white')

    net.from_nx(sub)

    net.repulsion(node_distance=420, central_gravity=0.33,
                           spring_length=110, spring_strength=0.10,
                           damping=0.95)

    net.show('net.html')

    HtmlFile = open('net.html', 'r', encoding='utf-8')

    components.html(HtmlFile.read(), height=600, width=600)

    st.balloons()

