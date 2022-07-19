import streamlit as st
import pandas as pd
import numpy as np

from get_address_details import Get_address_details, get_txn_counts
from ploty import  plot_single_address_txns

from streamlit_echarts import st_echarts

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

if st.sidebar.button("Vitalik.eth"):
    input_address = st.sidebar.text_input("Ether Address below", value = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
else:
    input_address = st.sidebar.text_input("Ether Address below", value = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    


### TXNS ACTIVITIES ###
if len(input_address) == 42:

    get_address_details = Get_address_details(input_address)
    address_df = get_address_details.get_all_txns()

    row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
    with row4_1:
        st.subheader('Analysis address txns')

    row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))

    with row5_1:
        st.markdown('You can change important parameters')   
        txn_type = ["all", "normal", "internal"]
        txn_type_button = st.selectbox("Tracing what kinds of transactions ?", txn_type)

        txn_time = ["all", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]
        txns_time_button = st.selectbox("Tracing time period", txn_time)

        st.markdown("More balance details could be found [DeBank](https://debank.com/profile/{})".format(input_address))

        normal_counts = len(address_df[address_df["txn_type"]=="normal"])
        internal_counts = len(address_df[address_df["txn_type"]=="internal"])
        total_counts = normal_counts + internal_counts
        
        st.metric(label="All Normal Txns", value="{} | {:.1f}%".format(normal_counts, 100*normal_counts/total_counts))
        st.metric(label="All Internal Txns", value="{} | {:.1f}%".format(internal_counts, 100*internal_counts/total_counts))

    with row5_2 :
        address_df_plot = get_txn_counts(address_df, txn_type_button, txns_time_button)
        plot_single_address_txns(address_df_plot, txns_time_button)


    row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))

    with row6_1:
        st.subheader('Dig Deeper')

    row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3, row7_3, row7_spacer4  = st.columns((1, 2, 1, 2, 1, 2, 1))

    with row7_1:
        test_time_year = ["2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]
        txns_time_year = st.selectbox("Tracing time period", test_time_year)

    with row7_2:
        test_time_month = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        txns_time_month = st.selectbox("Tracing time period", test_time_month)

    with row7_3:
        txns_type = ["normal", "internal"]
        txns_type = st.selectbox ("Tracing what kinds of transactions ?", txns_type)

    row8_spacer1, row8_1, row8_spacer2, row8_2, row8_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
    with row8_1:
        options = {
                    "title": {"text": "某站点用户访问来源", "subtext": "纯属虚构", "left": "center"},
                    "tooltip": {"trigger": "item"},
                    "legend": {
                        "orient": "vertical",
                        "left": "left",
                    },
                    "series": [
                            {
                                "name": "访问来源",
                                "type": "pie",
                                "radius": "50%",
                                "data": [
                                    {"value": 1048, "name": "搜索引擎"},
                                    {"value": 735, "name": "直接访问"},
                                    {"value": 580, "name": "邮件营销"},
                                    {"value": 484, "name": "联盟广告"},
                                    {"value": 300, "name": "视频广告"},
                                ],
                                "emphasis": {
                                    "itemStyle": {
                                        "shadowBlur": 10,
                                        "shadowOffsetX": 0,
                                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                                    }
                                },
                            }
                                    ],
                    }

        st.markdown("Select a legend, see the detail")
        events = {
            "legendselectchanged": "function(params) { return params.selected }",
        }
        s = st_echarts(
            options=options, events=events, height="600px", key="render_pie_events"
        )
        if s is not None:
            st.write(s)
    
    with row8_2:
        st.table(address_df.head(3))

    row9_spacer1, row9_1, row9_spacer2 = st.columns((.2, 7.1, .2))

    with row9_1:
        contactname_list = list(address_df.columns)
        contract_button = st.selectbox("Select a Contract to see details", contactname_list)
        st.table(address_df[contract_button].head(5))

else:
    st.markdown("Give us valid address !")