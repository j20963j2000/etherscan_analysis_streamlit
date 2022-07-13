import streamlit as st
import pandas as pd
import numpy as np

from get_address_details import Get_address_details

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
address = st.sidebar.text_input("Ether Address")