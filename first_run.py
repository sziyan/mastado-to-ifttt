import requests
from config import Config

instance_url = Config.instance_url
access_token = Config.access_token
headers = {'Authorization': 'Bearer {}'.format(access_token)}

def get_id():
    url = '{}/api/v1/accounts/verify_credentials'.format(instance_url)
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get('id')

def get_status(account_id):
    url = '{}/api/v1/accounts/{}/statuses'.format(instance_url,account_id)
    params = {'exclude_reblogs': True, 'limit': 1}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    return data

#get latest status
first_status = get_status(get_id())[0]
#get status id
first_status_id = first_status.get('id')

#write to file
with open('latest_status.txt', 'w') as f:
    f.writelines(first_status_id)
f.close()
print('latest_status.txt created!')