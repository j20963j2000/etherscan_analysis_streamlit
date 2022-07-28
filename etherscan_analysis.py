import streamlit as st
import pandas as pd
import numpy as np

from get_address_details import Get_address_details, get_txn_counts, get_contract_df, add_contract_url, count_contra_values, known_address, check_button_status
from ploty import  plot_single_address_txns
from control_botton_config import row7_txn_month_config

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
    st.markdown("Let's start tracing !  👇👇👇")


#################
### SELECTION ###
#################

from PIL import Image
image = Image.open('ether.png')

st.sidebar.image(image, output_format ="PNG")
st.sidebar.text('')
st.sidebar.text('')

### INPUT ADDRESS ###

st.sidebar.header("**Who you want to trace ?**")

# 0x5314c8991d3AcB5d5245Ae8D1320191e8EB0454c

user_input = st.sidebar.text_input("Ether Address below")
if user_input != "":
    st.session_state.input_address = user_input
if st.sidebar.button("Vitalik.eth", key = "1"):
    st.session_state.input_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
if st.sidebar.button("Vb2", key = "2"):
    st.session_state.input_address = "0x1db3439a222c519ab44bb1144fc28167b4fa6ee6"
if st.sidebar.button("SBF", key = "3"):
    st.session_state.input_address = "0x477573f212a7bdd5f7c12889bd1ad0aa44fb82aa"
if st.sidebar.button("Stephen Curry", key = "4"):
    st.session_state.input_address = "0x3becf83939f34311b6bee143197872d877501b11"


### TXNS ACTIVITIES ###
if "input_address" in st.session_state and len(st.session_state.input_address) == 42:

    input_address = st.session_state.input_address.lower()

    get_address_details = Get_address_details(input_address)

    try:
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
            
            st.text("")
            st.text("")
            st.text("")
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
            txns_type = ["normal", "internal"]
            txns_type_botton = st.selectbox ("Tracing what kinds of transactions ?", txns_type)

        with row7_2:

            txns_year = ["2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]
            txns_year_botton = st.selectbox("Tracing time period", txns_year)

        with row7_3:
        
            txns_month_botton = st.selectbox("Tracing time period", row7_txn_month_config(txns_year_botton))

        # row8_spacer1, row8_1, row8_spacer2, row8_2, row8_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
        row8_spacer1, row8_1, row8_spacer2 = st.columns((.2, 7.1, .2))
        
        try:
            contract_df, contract_name = get_contract_df(input_address, address_df, str(txns_type_botton), str(txns_year_botton), str(txns_month_botton))
            pie_list, statis_df = count_contra_values(contract_df)
        except:
            st.info("No Internal Data found")

        with row8_1:
            try:
                options = {
                            "title": {"text": "Smart Contract interaction distribution", "subtext": "{}-{}".format(txns_year_botton, txns_month_botton), "left": "center"},
                            "tooltip": {"trigger": "item"},
                            "legend": {
                                "orient": "vertical",
                                "left": "left",
                            },
                            "series": [
                                    {
                                        "name": "Contract Name",
                                        "type": "pie",
                                        "radius": "50%",
                                        # "data": [
                                        #     {"value": 1048, "name": "搜索引擎"},
                                        #     {"value": 735, "name": "直接访问"},
                                        #     {"value": 580, "name": "邮件营销"},
                                        #     {"value": 484, "name": "联盟广告"},
                                        #     {"value": 300, "name": "视频广告"},
                                        # ],
                                        "data": pie_list,
                                        "emphasis": {
                                            "itemStyle": {
                                                "shadowBlur": 200,
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
            except:
                st.write("No Data Found")
        # with row8_2:
        #     st.table(statis_df)
        # test_df = contract_df.insert(0, "url", "[Jackson Yin](https://www.linkedin.com/in/jackson-yin)")
        row9_spacer1, row9_1, row9_spacer2 = st.columns((.2, 7.1, .2))

        with row9_1:
            try:
                contactname_list = set(contract_name.values())
                contract_button = st.selectbox("Select a Contract to see details", contactname_list)

                contract_detail_df = contract_df.copy(deep = True)
                # st.write(contract_detail_df)
                select_contract_df = contract_detail_df[contract_detail_df.ContractName == contract_button]
                # st.write(select_contract_df)
                select_contract_df = add_contract_url(select_contract_df)
                # add_contract_url(select_contract_df)
                # print(select_contract_df)
                # st.markdown(select_contract_df)
                # st.write(select_contract_df.to_markdown())
                st.write(select_contract_df)
                # st.write((contract_df[contract_df.ContractName == contract_button]).to_markdown())
            except :
                st.info("No data")
    except :
        st.info("Please try again")
else:
    st.info("Give us valid address !")