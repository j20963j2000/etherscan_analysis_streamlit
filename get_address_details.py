from calendar import c
import pandas as pd
from requests import get
from datetime import datetime
import streamlit as st

API_KEY = "PER4V6RYCAU4TZ54M69D9GXHWNVKX6DY7Z"
BASE_URL = "https://api.etherscan.io/api"
ETHER_VALUE = 10 ** 18

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

def make_sourcecode_api_url(address, **kwargs):
    url = BASE_URL + f"?module=contract&action=getsourcecode&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url

def get_contract_name(contract_address):
    responce = get(make_sourcecode_api_url(contract_address)).json()
    name = responce["result"][0]["ContractName"]
    return name

def get_txn_counts(address_df, txn_type, txn_time):

    if txn_type == "all" and txn_time == "all":
        year_list = {str(i):len(address_df.loc[str(i)]) for i in range(2015, 2023)}
        result = pd.DataFrame(list(year_list.items()), columns = ["year", "counts"])
        return result
    
    elif txn_type == "all" and txn_time != "all":
        year_list_output = {str(month):0 for month in range(1, 13)}
        month_count = {str(i):len(address_df.loc["{}-{}".format(txn_time, i)]) for i in range(1, 13)}
        year_list_output.update(month_count)
        result = pd.DataFrame(list(year_list_output.items()), columns = ["month", "counts"])
        return result
    
    elif txn_type != "all" and txn_time == "all":
        mask = address_df["txn_type"] == txn_type
        year_list = {str(i):len(address_df[mask].loc[str(i)]) for i in range(2015, 2023)}
        result = pd.DataFrame(list(year_list.items()), columns = ["year", "counts"])
        return result

    else:            
        year_list_output = {str(month):0 for month in range(1, 13)}

        for i in range(1, 13):
            tmp_df = address_df.loc["{}-{}".format(txn_time, i)]
            tmp_mask = tmp_df["txn_type"] == txn_type
            year_list_output[str(i)] = len(tmp_df[tmp_mask])

        result = pd.DataFrame(list(year_list_output.items()), columns = ["month", "counts"])
        return result

def get_contract_df(target_address, address_df, txn_type, txn_year, txn_month):
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
        st.write("No Data Found")

def add_contract_url(contra_df):

    for i in range(len(contra_df)):
        contra_ads = contra_df["ads"][i]
        name = contra_df["ContractName"][i]
        url = "https://etherscan.io/address/{}".format(contra_ads)
        contra_df.loc[i, "ContractName"] = "[{}]({})".format(name, url)
        
    return contra_df.to_markdown()