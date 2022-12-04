import requests
from config import Config
import html2text
import time
import logging
logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a', format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %I:%M:%S %p')
logger = logging.getLogger(__name__)

instance_url = Config.instance_url
access_token = Config.access_token
ifttt_webhook_key = Config.ifttt_webhook_key
ifttt_event = Config.ifttt_event
headers = {'Authorization': 'Bearer {}'.format(access_token)}

def get_id():
    url = '{}/api/v1/accounts/verify_credentials'.format(instance_url)
    r = requests.get(url, headers=headers)
    data = r.json()
    return data.get('id')

def get_status(account_id):
    latest_id = check_latest_status_id()
    url = '{}/api/v1/accounts/{}/statuses'.format(instance_url,account_id)
    params = {'exclude_reblogs': True, 'since_id': '{}'.format(latest_id)}
    #params = {'exclude_reblogs': True, 'limit': 5}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    return data

def clean_html(content):
    h = html2text.HTML2Text()
    h.ignore_links = True
    clean_content = h.handle(content)
    return clean_content

def check_latest_status_id():
    with open('latest_status.txt') as f:
        line = f.readline()
        latest_status_id = line
    f.close()
    return latest_status_id

def write_status_id(status_id):
    with open('latest_status.txt', 'w') as f:
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

def check_if_mention(mentions):
    if not bool(mentions):
        #status no mentions
        return False
    else:
        #status have mentions
        return True

logging.info('Starting bot')
print('Starting bot')


while True:
    #get latest statuses
    statuses = get_status(get_id())

    #loop through each status
    for i in reversed(statuses):
        #check if status have mentions
        if check_if_mention(i.get('mentions')) is False:
            #get the content of the status as there are no mentions
            content = i.get('content')
            clean_content = clean_html(content)
            media_attachments = i.get('media_attachments')
            if media_attachments:
                image_url = media_attachments[0].get('url')
                send_ifttt_webhook(clean_content, image_url=image_url)
            else:
                send_ifttt_webhook(clean_content)
            print(clean_content)
            logging.info(clean_content)
            time.sleep(12)
        else:
            print('Skipping mentions status - {}'.format(i.get('content')))
            logging.info('Skipping mentions status - {}'.format(i.get('content')))
        #write the latest status id to txt file
        write_status_id(i.get('id'))
        #sleep few seconds as IFTTT takes 10sec to trigger 
    time.sleep(60)

