import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker



def plot_single_address_txns(address_result): #total #against, #conceived
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
        df = pd.DataFrame(list(address_result.items()),
                    columns=['datetime', 'counts'])

        plt.rcParams.update(rc)
        fig, ax = plt.subplots()
        
        ax = sns.barplot(x="datetime", y="counts", data=df)
        # tick_spacing = len(df)/5 # x軸密集度
        # ax.xaxis.set_major_locator(mticker.MultipleLocator(12))
        # y_str = measure + " " + attr + " " + "per Game"
        # if measure == "Absolute":
        #     y_str = measure + " " + attr
        # if measure == "Minimum" or measure == "Maximum":
        #     y_str = measure + " " + attr + "in a Game"
        # ax.set(xlabel = "Team", ylabel = y_str)
        # plt.xticks(rotation=66,horizontalalignment="right")
        # if measure == "Mean" or attribute in ["distance","pass_ratio","possession","tackle_ratio"]:
        #     for p in ax.patches:
        #         ax.annotate(format(p.get_height(), '.2f'), 
        #               (p.get_x() + p.get_width() / 2., p.get_height()),
        #                ha = 'center',
        #                va = 'center', 
        #                xytext = (0, 18),
        #                rotation = 90,
        #                textcoords = 'offset points')
        # else:
        #     for p in ax.patches:
        #         ax.annotate(format(str(int(p.get_height()))), 
        #               (p.get_x() + p.get_width() / 2., p.get_height()),
        #                ha = 'center',
        #                va = 'center', 
        #                xytext = (0, 18),
        #                rotation = 90,
        #                textcoords = 'offset points')
        st.pyplot(fig)
    except:
        st.markdown("No Data")
