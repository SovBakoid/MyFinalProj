import re
import streamlit as st

rus_letters=["А", "В", "Е", "К", "М", "Н", "О", "Р", "С", "Т", "У", "Х"]

digits=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

for i in digits:
    st.write(bool(re.match(f'[А-Я]+{i}{i}{i}[А-Я]+\d+', "А555ВС777")))

st.write(bool(None))






