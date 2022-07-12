import streamlit as st
import pandas as pd
import numpy as np

st.title('Etherscan Analysis')

API_KEY = "PER4V6RYCAU4TZ54M69D9GXHWNVKX6DY7Z"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18