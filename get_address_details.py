from requests import get
from datetime import datetime

class Get_address_details():
    """
    Get the following informations from a single address:
        - balance
        - all txns
        - normal txns
        - internal txns
    """
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
    
    def get_account_balance(self):
        balance_url = self.make_api_url("account", "balance", tag="latest")
        response = get(balance_url)
        data = response.json()

        value = int(data["result"]) / ETHER_VALUE
        return value
    
    def get_all_txns(self):
        """
        Get all txns 
        """
        transactions_url = self.make_api_url("account", "txlist", startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
        response = get(transactions_url)
        data = response.json()["result"]

        internal_tx_url = self.make_api_url("account", "txlistinternal", startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
        response2 = get(internal_tx_url)
        data2 = response2.json()["result"]

        data.extend(data2)
        data.sort(key=lambda x: int(x['timeStamp']))

        return data
    
    def get_txns_sum_by_datetime(self):
        address_data = self.get_all_txns()
        txns_by_datetime = {}

        for txn_data in address_data:
            time = str(datetime.fromtimestamp(int(txn_data["timeStamp"]))).split(" ")[0]

            if time in txns_by_datetime:
                txns_by_datetime[time] += 1
            else:
                txns_by_datetime[time] = 1
        return txns_by_datetime
    
    def get_normal_txns_by_datetime(self):
    
        """
        Get normal txns by date time
        """

        txns_by_datetime = {}

        transactions_url = self.make_api_url("account", "txlist", startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
        response = get(transactions_url)
        data = response.json()["result"]

        data.sort(key=lambda x: int(x['timeStamp']))

        for d in data:
            time = str(datetime.fromtimestamp(int(d["timeStamp"]))).split(" ")[0]

            if time in txns_by_datetime:
                txns_by_datetime[time] += 1
            else:
                txns_by_datetime[time] = 1

        return txns_by_datetime
    
    def get_internal_txns_by_datetime(self):
    
        """
        Get normal txns by date time
        """

        txns_by_datetime = {}

        transactions_url = self.make_api_url("account", "txlistinternal", startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
        response = get(transactions_url)
        data = response.json()["result"]

        data.sort(key=lambda x: int(x['timeStamp']))

        for d in data:
            time = str(datetime.fromtimestamp(int(d["timeStamp"]))).split(" ")[0]

            if time in txns_by_datetime:
                txns_by_datetime[time] += 1
            else:
                txns_by_datetime[time] = 1

        return txns_by_datetime