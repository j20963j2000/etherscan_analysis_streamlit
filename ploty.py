import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt




# def plot_x_per_team(attr,measure): #total #against, #conceived
#     rc = {'figure.figsize':(8,4.5),
#           'axes.facecolor':'#0e1117',
#           'axes.edgecolor': '#0e1117',
#           'axes.labelcolor': 'white',
#           'figure.facecolor': '#0e1117',
#           'patch.edgecolor': '#0e1117',
#           'text.color': 'white',
#           'xtick.color': 'white',
#           'ytick.color': 'white',
#           'grid.color': 'grey',
#           'font.size' : 8,
#           'axes.labelsize': 12,
#           'xtick.labelsize': 8,
#           'ytick.labelsize': 12}
    
#     plt.rcParams.update(rc)
#     fig, ax = plt.subplots()
#     ### Goals
#     attribute = label_attr_dict_teams[attr]
#     df_plot = pd.DataFrame()
#     df_plot = group_measure_by_attribute("team",attribute,measure)
#     if specific_team_colors:
#         ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), palette = color_dict)
#     else:
#         ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), color = "#b80606")
#     y_str = measure + " " + attr + " " + "per Game"
#     if measure == "Absolute":
#         y_str = measure + " " + attr
#     if measure == "Minimum" or measure == "Maximum":
#         y_str = measure + " " + attr + "in a Game"
#     ax.set(xlabel = "Team", ylabel = y_str)
#     plt.xticks(rotation=66,horizontalalignment="right")
#     if measure == "Mean" or attribute in ["distance","pass_ratio","possession","tackle_ratio"]:
#         for p in ax.patches:
#             ax.annotate(format(p.get_height(), '.2f'), 
#                   (p.get_x() + p.get_width() / 2., p.get_height()),
#                    ha = 'center',
#                    va = 'center', 
#                    xytext = (0, 18),
#                    rotation = 90,
#                    textcoords = 'offset points')
#     else:
#         for p in ax.patches:
#             ax.annotate(format(str(int(p.get_height()))), 
#                   (p.get_x() + p.get_width() / 2., p.get_height()),
#                    ha = 'center',
#                    va = 'center', 
#                    xytext = (0, 18),
#                    rotation = 90,
#                    textcoords = 'offset points')
#     st.pyplot(fig)
