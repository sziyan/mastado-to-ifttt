import requests
from config import Config
import html2text
import time
import logging
logging.basicConfig(level=logging.INFO, filename='pixelfed.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
logger = logging.getLogger(__name__)

instance_url = Config.pixelfed_instance_url
pixel_access_token = Config.pixel_access_token
ifttt_webhook_key = Config.ifttt_webhook_key
ifttt_event = Config.ifttt_event
headers = {'Authorization': 'Bearer {}'.format(pixel_access_token)}
latest_status_id_filename = 'pixelfed_latest_status.txt'

def get_id():
    url = '{}/api/v1/accounts/verify_credentials'.format(instance_url)
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get('id')

def clean_html(content):
    h = html2text.HTML2Text()
    h.ignore_links = True
    clean_content = h.handle(content)
    return clean_content

def send_request(url, headers=None, data=None):
    r = requests.get(url, headers=headers, data=data)
    data = r.json()
    return data

def check_latest_status_id():
    with open(latest_status_id_filename) as f:
        line = f.readline()
        latest_status_id = line
    f.close()
    return latest_status_id

def get_status(account_id):
    latest_id = check_latest_status_id()
    url = '{}/api/v1/accounts/{}/statuses'.format(instance_url,account_id)
    params = {'min_id': '504902185668143713', 'limit': 5}
    # params = {'exclude_reblogs': True, 'limit': 1}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    return data

def write_status_id(status_id):
    with open(latest_status_id_filename, 'w') as f:
        f.write(status_id)
    f.close()

def send_ifttt_webhook(content, image_url=None):
    url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'.format(ifttt_event,ifttt_webhook_key)
    if image_url:
        data = {'value1': content, 'value2': image_url}
    else:
        data = {'value1': content}
    r = requests.post(url, data=data)
    return

# testing
statuses = get_status(get_id())
for i in reversed(statuses):
    print(i.get('id'))
    print(i.get('content'))

# logging.info('Starting bot')
# print('Starting bot')

# while True:
#     #get latest statuses
#     statuses = get_status(get_id())
#     #loop through each status
#     for i in reversed(statuses):
#         content = i.get('content')
#         clean_content = clean_html(content)
#         #only get first media since IFTTT DayOne only support 1 image URL
#         media_attachments = i.get('media_attachments')[0]
#         image_url = media_attachments.get('url')
#         send_ifttt_webhook(clean_content, image_url=image_url)
#         print(clean_content)
#         logging.info(clean_content)
#         time.sleep(12)
#         #write the latest status id to txt file
#         write_status_id(i.get('id'))
#         #sleep few seconds as IFTTT takes 10sec to trigger 
#     time.sleep(60)

