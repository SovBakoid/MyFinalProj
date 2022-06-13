import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

with st.echo(code_location="below"):

    st.header("Машинка((( :face_with_one_eyebrow_raised:")

    with open('flats_moscow.csv', "rb") as f:
        data_from_hse=pd.read_csv(f)

    data_from_hse=data_from_hse.drop(columns=["Unnamed: 0", "code"])

    data_from_hse["price"]=data_from_hse["price"].astype("float64")
    data_from_hse["totsp"]=data_from_hse["totsp"].astype("float64")
    data_from_hse["livesp"]=data_from_hse["livesp"].astype("float64")
    data_from_hse["kitsp"]=data_from_hse["kitsp"].astype("float64")
    data_from_hse["dist"]=data_from_hse["dist"].astype("float64")
    data_from_hse["metrdist"]=data_from_hse["metrdist"].astype("int64")
    data_from_hse["walk"]=data_from_hse["walk"].astype("int64")
    data_from_hse["brick"]=data_from_hse["brick"].astype("int64")
    data_from_hse["floor"]=data_from_hse["floor"].astype("int64")

    st.write("Я взял вот такой датасэт (https://www.kaggle.com/code/vitalykuleshov/regression-analysis-the-price-of-moscow-flats) с данными про стоимость квартир в Москве.")

    a=data_from_hse.head()
    a

    st.write("""Легенда:
     
    price — цена квартиры в $1000,
     
    totsp — общая площадь квартиры, кв.м., 
    
    livesp — жилая площадь квартиры, кв.м.,
    
    kitsp — площадь кухни, кв.м.,
    
    dist — расстояние от центра в км.,
    
    metrdist — расстояние до метро в минутах,
    
    walk — 1 – пешком от метро, 0 – на транспорте,
    
    brick — 1 – кирпичный, монолит ж/б, 0 – другой,
    
    floor — 1 – этаж кроме первого и последнего, 0 – иначе.""")

    st.write("В сиборне получается вот такая карта корреляций.")

    ###FROM: https://seaborn.pydata.org/examples/many_pairwise_correlations.html

    sns.set_theme(style="white")

    corr_data=data_from_hse.corr()

    mask = np.triu(np.ones_like(corr_data, dtype=bool))

    fig, ax=plt.subplots(figsize=(11, 9))

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(corr_data, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    ###END FROM

    st.pyplot(fig)

    train, test = train_test_split(data_from_hse, test_size=0.2)

    train_price=train["price"]

    train=train.drop(columns="price")

    test_price=test["price"]

    test=test.drop(columns="price")

    xgtrain = xgb.DMatrix(train.values, train_price.values)

    xgtest = xgb.DMatrix(test.values)

    params = {'booster': 'gblinear', 'objective': 'reg:linear',
          'max_depth': 2, 'learning_rate': .1, 'n_estimators': 500,    'min_child_weight': 3, 'colsample_bytree': .7,
          'subsample': .8, 'gamma': 0, 'reg_alpha': 1}

    model = xgb.train(dtrain=xgtrain, params=params)

    predictions = model.predict(xgtest)

    r2 = r2_score(test_price.to_numpy(), predictions)

    #accuracy=int(accuracy*100)

    st.write("Далее я обучил (код как всегда ниже) модель на рандомной выборке, составляющей 4/5 всего датасэта и проверил на оставшихся.")

    st.write(f"Получилось, что моя полученная модель имеет r2 score = {r2}")