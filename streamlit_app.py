import streamlit as st
import numpy as np
import pandas as pd
import datetime

usdrub = 74

import locale
locale.setlocale( locale.LC_ALL, 'EN-gb' )
def rub(x):
    return locale.format_string('%g',val=x,grouping=True)+' rub'

d0 = datetime.datetime.today().date()
d1 = (d0 + datetime.timedelta(days=30*6)
      ).strftime('%Y-%m-%d')
d2 = (d0 + datetime.timedelta(days=30*12)
      ).strftime('%Y-%m-%d')
d0 = d0.strftime('%Y-%m-%d')

bonus_t = pd.DataFrame({
    '1p': [0.65,0.75,0.8,0.9,0.9], 
    '2p': [0.9,1.05,1.15,1.25,1.25],
    '3p': [1.3,1.5,1.6,1.8,1.8],
    '4p': [1.85,2.1,2.25,2.25,2.25,]
},index=[14,15,16,17,18])

rsu_t = pd.DataFrame({ 
    '1p': [0,0,5500,11000,24500],
    '2p': [0,5500,7800,15600,34600],
    '3p': [0,7800,11000,22000,49000],
    '4p': [0,11000,15600,31100,69300]
},index=[14,15,16,17,18])

#Inputs

grade = st.sidebar.selectbox(
    'Your grade',
    (14,15,16,17,18)
)

salary = st.sidebar.number_input(
    'Your month salary',
    value=150000,step=1000
)

assessment = st.sidebar.selectbox(
    'Your desire review assessment',
    ('1p','2p','3p','4p',)
)

bonus = int( salary * bonus_t.loc[grade,assessment] )
bonus_m = int(bonus/6)
rsu = int( rsu_t.loc[grade,assessment]*0.87*usdrub )
rsu_m = int(rsu/48)

result_t = pd.DataFrame({
    'salary': [salary,salary,salary]
    ,'bonus': [0,bonus_m,0]
    ,'rsu': [0,rsu_m,rsu_m]
#},index=[d0,d1,d2])
},index=['0_today','1_after review','2_after next review'])


#Frontend

st.header('Y review calculator')

if rsu == 0:
    st.warning('Your assessment is too low to get an RSU 😒')

st.markdown(f'Your bonus for the next 6 month will be: {rub(bonus)}. Equal to {rub(bonus_m)} per month adding to salary')
st.markdown(f'Your RSU for the next 4 years will be: {rub(rsu)}. Equal to {rub(rsu_m)} per month adding to salary')
st.markdown(f'Total salary: **{rub(salary+bonus_m+rsu_m)}**' )

st.subheader('Forecasted month earnngs')
st.bar_chart(result_t)