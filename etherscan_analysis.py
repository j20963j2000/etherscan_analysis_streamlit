import streamlit as st
import pandas as pd
import numpy as np

from get_address_details import Get_address_details
from ploty import  plot_single_address_txns

st.set_page_config(layout="wide")


####################
### INTRODUCTION ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('EtherTrace - Tracing Etherscan activities')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Jackson Yin](https://www.linkedin.com/in/jackson-yin)')

row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Hello tracers, this app could help you to trace activities for any address on Etherscan.")
    st.markdown("Let's start tracing ! ** 👇")


#################
### SELECTION ###
#################

st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

### INPUT ADDRESS ###

st.sidebar.markdown("**Who you want to trace ?**")
input_address = st.sidebar.text_input("Ether Address", value = "0x73bceb1cd57c711feac4224d062b0f6ff338501e")
get_address_details = Get_address_details(input_address)


### TXNS ACTIVITIES ###
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Analysis address txns')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))

with row5_1:
    st.markdown('You can change important parameters')   
    txns_type = ["all", "normal", "internal"]
    txns_type = st.selectbox ("Tracing what kinds of transactions ?", txns_type)

    test_time = ["all", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]
    txns_time = st.selectbox("Tracing time period", test_time)

with row5_2:
    if txns_type == "all":
        address_result = get_address_details.get_txns_by_year(txns_time)
        plot_single_address_txns(address_result)
    else:
        address_result = get_address_details.get_nor_itn_txns_by_year(txns_type, txns_time)
        plot_single_address_txns(address_result)