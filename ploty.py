import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
from streamlit_echarts import st_echarts


def plot_single_address_txns(address_result, txn_time): #total #against, #conceived
    rc = {'figure.figsize':(7,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 8,
          'axes.labelsize': 12,
          'xtick.labelsize': 8,
          'ytick.labelsize': 10}
    try:
        # print("address_result :", address_result)
        plt.rcParams.update(rc)
        fig, ax = plt.subplots()
        
        if txn_time == "all":
            ax = sns.barplot(x="year", y="counts", data=address_result)
            ax.bar_label(ax.containers[0])
        
        else:
            ax = sns.barplot(x="month", y="counts", data=address_result)
            ax.bar_label(ax.containers[0])
            
        st.pyplot(fig)

    except:
        st.markdown("No Data")
