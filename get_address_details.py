import pandas as pd
from requests import get
from datetime import datetime
import streamlit as st

API_KEY = "PER4V6RYCAU4TZ54M69D9GXHWNVKX6DY7Z"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

@st.cache
class Get_address_details():
    
    def __init__(self, address):
       
        self.address = address
        self.BASE_URL = "https://api.etherscan.io/api"
        self.ETHER_VALUE = 10 ** 18
        self.API_KEY = "PER4V6RYCAU4TZ54M69D9GXHWNVKX6DY7Z"
        
    def make_api_url(self, module, action, **kwargs):
        url = self.BASE_URL + f"?module={module}&action={action}&address={self.address}&apikey={self.API_KEY}"

        for key, value in kwargs.items():
            url += f"&{key}={value}"

        return url
    
    def make_hash_api_url(self, module, action, txhash, **kwargs):
        url = self.BASE_URL + f"?module={module}&action={action}&txhash={txhash}&apikey={self.API_KEY}"
        
        for key, value in kwargs.items():
            url += f"&{key}={value}"

        return url
    
    def get_txns_from_txnhash(self, txhash):
        txn_url = self.make_hash_api_url("account", "txlistinternal", txhash)
        responce = get(txn_url)
        data = responce.json()
        
        return data["result"]
        
    def get_account_balance(self):
        balance_url = self.make_api_url("account", "balance", tag="latest")
        response = get(balance_url)
        data = response.json()

        value = int(data["result"]) / self.ETHER_VALUE
        return value
    
    def get_all_txns(self):
        """
        Get all txns 
        """
        transactions_url = self.make_api_url("account", "txlist", startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
        response = get(transactions_url)
        nor_data = response.json()["result"]
        nor_df = pd.DataFrame(nor_data)
        nor_df.insert(1, "txn_type", value ="normal")
        
        internal_tx_url = self.make_api_url("account", "txlistinternal", startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
        in_response = get(internal_tx_url)
        in_data = in_response.json()["result"]
        in_df = pd.DataFrame(in_data)
        in_df.insert(1, "txn_type", value = "internal")
        
        data_df = pd.concat([nor_df, in_df], join = "outer")
        
        new_time_list = []
        for idx, timestamp in enumerate(data_df["timeStamp"]):
            data_df["timeStamp"][idx] = int(timestamp)
            new_time = str(datetime.fromtimestamp(int(timestamp))).split(" ")[0]
            new_time_list.append(new_time)

        data_df.insert(1, "datetime", new_time_list)
        data_df["datetime"] = pd.to_datetime(data_df["datetime"])
        data_df = data_df.sort_index()
        
        date_df_out = data_df.set_index("datetime")

        return date_df_out

@st.cache
def make_sourcecode_api_url(address, **kwargs):
    url = BASE_URL + f"?module=contract&action=getsourcecode&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url

@st.cache
def get_contract_name(contract_address):
    responce = get(make_sourcecode_api_url(contract_address)).json()
    name = responce["result"][0]["ContractName"]
    return name

@st.cache
def get_txn_counts(address_df, txn_type, txn_time):

    if txn_type == "all" and txn_time == "all":
        year_list_output = {str(year):0 for year in range(2015, 2023)}

        for i in range(2015, 2023):
            try:
                tmp_df = address_df.loc["{}".format(i)]
                # tmp_mask = tmp_df["txn_type"] == txn_type
                year_list_output[str(i)] = len(tmp_df)
            except:
                pass

        result = pd.DataFrame(list(year_list_output.items()), columns = ["year", "counts"])
        return result
    
    elif txn_type == "all" and txn_time != "all":
        year_list_output = {str(month):0 for month in range(1, 13)}

        for i in range(1, 13):
            try:
                tmp_df = address_df.loc["{}-{}".format(txn_time, i)]
                # tmp_mask = tmp_df["txn_type"] == txn_type
                year_list_output[str(i)] = len(tmp_df)
            except:
                pass

        result = pd.DataFrame(list(year_list_output.items()), columns = ["month", "counts"])
        return result
    
    elif txn_type != "all" and txn_time == "all":
        year_list_output = {str(year):0 for year in range(2015, 2023)}

        for i in range(2015, 2023):
            try:
                tmp_df = address_df.loc["{}".format(i)]
                tmp_mask = tmp_df["txn_type"] == txn_type
                year_list_output[str(i)] = len(tmp_df[tmp_mask])
            except:
                pass

        result = pd.DataFrame(list(year_list_output.items()), columns = ["year", "counts"])
        return result

    else:            
        year_list_output = {str(month):0 for month in range(1, 13)}

        for i in range(1, 13):
            try:
                tmp_df = address_df.loc["{}-{}".format(txn_time, i)]
                tmp_mask = tmp_df["txn_type"] == txn_type
                year_list_output[str(i)] = len(tmp_df[tmp_mask])
            except:
                pass

        result = pd.DataFrame(list(year_list_output.items()), columns = ["month", "counts"])
        return result

@st.cache
def get_contract_df(target_address, address_df, txn_type, txn_year, txn_month):
    # for both normal and internal transactions
    mask = address_df["txn_type"] == txn_type
    tmp_df = address_df[mask].loc[txn_year+"-"+txn_month]

    contarct_list = []
    contarct_set = set()
    if len(tmp_df) != 0:
        for data in tmp_df.iterrows(): 
            
            from_ads = data[1][7]
            to_ads = data[1][8]

            contarct_set.add(from_ads)
            contarct_set.add(to_ads)

            hash = data[1][3]
            value = int(data[1][9])/(10 ** 18)
            if from_ads == target_address.lower():
                tmp_contract_dict = {"hash":hash, "ads":to_ads, "value(ETH)":value}
            if to_ads == target_address.lower():
                tmp_contract_dict = {"hash":hash, "ads":from_ads, "value(ETH)":value}
            contarct_list.append(tmp_contract_dict)

        contarct_set.remove(target_address.lower())
        contract_df = pd.DataFrame(contarct_list)
        contract_name = {}
        for i in contarct_set:
            name = get_contract_name(i)
            if name == "":
                contract_name[i] = "unknown"
            else:
                contract_name[i] = name
        contract_df.insert(0, "ContractName", "unknown")
        for ads in contract_name:
            # df.loc[df.grades>50,'result']='success'
            contract_df.loc[contract_df.ads == ads, "ContractName"] = contract_name[ads]
        return contract_df, contract_name
    else:
        # st.write("No Data Found")
        pass

# @st.cache
def add_contract_url(contra_df):
    output_df = contra_df.copy(deep = True)
    output_df.reset_index(inplace = True, drop = True)
    for i in range(len(output_df)):
        # st.write("i :", i)
        # st.write(output_df)
        hash = output_df["hash"][i]
        contra_ads = output_df["ads"][i]
        name = output_df["ContractName"][i]
        url = "https://etherscan.io/address/{}".format(contra_ads)
        hash_url = "https://etherscan.io/tx/{}".format(hash)
        output_df.loc[i, "ContractName"] = "[{}]({})".format(name, url)
        output_df.loc[i, "hash"] = "[{}]({})".format("Transaction details", hash_url)
        # st.write(output_df)
    return output_df.to_markdown()
    # st.session_state.md_contra_df = output_df.to_markdown()
    # return output_df

@st.cache
def count_contra_values(contract_df):
    statis_df = {}
    contra_name = set(contract_df["ContractName"])
    
    for name in contra_name:
        if name in statis_df.keys():

            for i in range(len(contract_df)):
                if contract_df.loc[i, "ContractName"] == name:
                    value = contract_df.loc[i, "value(ETH)"]
                    statis_df[name] += float(value)
        else:
            statis_df[name] = 0

            for i in range(len(contract_df)):
                if contract_df.loc[i, "ContractName"] == name:
                    value = contract_df.loc[i, "value(ETH)"]
                    statis_df[name] += float(value)

    output_list = []

    for key in statis_df:
        tmp_df = {}
        tmp_df["name"] = key
        tmp_df["value"] = statis_df[key]
        output_list.append(tmp_df)
    
    return output_list, pd.DataFrame([statis_df])

@st.cache
def known_address(address_input):

    if st.sidebar.button("Vitalik.eth"):
        input_address = st.sidebar.text_input("Ether Address below", value = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
    elif st.sidebar.button("Vb2"):
        input_address = st.sidebar.text_input("Ether Address below", value = "0x1db3439a222c519ab44bb1144fc28167b4fa6ee6")
    else:
        input_address = st.sidebar.text_input("Ether Address below", value = address_input)
    
    input_address = input_address.lower()

@st.cache
def set_input_address():

    if st.sidebar.button("Vitalik.eth", key = "1"):
        input_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    if st.sidebar.button("Vb2", key = "2"):
        input_address = "0x1db3439a222c519ab44bb1144fc28167b4fa6ee6"
    if st.sidebar.button("SBF", key = "3"):
        input_address = "0x477573f212a7bdd5f7c12889bd1ad0aa44fb82aa"
    if st.sidebar.button("Stephen Curry", key = "4"):
        input_address = "0x3becf83939f34311b6bee143197872d877501b11"
    
    input_address = input_address.lower()
    
    return input_address

@st.cache
def check_button_status(bool):
    button_status = False

    return button_status