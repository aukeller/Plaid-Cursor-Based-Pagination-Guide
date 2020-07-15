from pprint import pprint
from plaid import Client

client = Client(client_id = '', secret = '', 
public_key = '', environment = 'sandbox')

# Offset pagination 

response = client.Transactions.get('access_token', 
                                   start_date='2020-01-01', 
                                   end_date='2020-06-01',
                                   count = 250, 
                                   offset = 1000)

# Cursor-based pagination for first 250 results

response = client.Transactions.get(access_token, 
                                   start_date='2020-01-01', 
                                   end_date='2020-06-01',
                                   count = 250, 
                                   cursor = None)

# Cursor-based pagination using the next_cursor from the previous response above

response = client.Transactions.get(access_token, 
                                   start_date='2020-01-01', 
                                   end_date='2020-06-01',
                                   count = 250, 
                                   cursor = "eyJNYXJrZXIiOiBudWxsLCAiYm90b190cnVuY2F0ZV9hbW91bnQiOiAxfQ")
