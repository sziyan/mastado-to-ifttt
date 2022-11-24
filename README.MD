# Simple script to read Mastado public and private statuses and trigger IFTTT webhook

## Configuration
1. Create `config.py` with the following:
```python
class Config:
    instance_url = '' #your mastadon instance url
    access_token = '' # your mastadon developer access token
    ifttt_webhook_key = '' # your ifttt webhook key
    ifttt_event = '' # your ifttt webhook trigger event name
```
2. Populate `config.py` with your configurations
3. Install dependencies from `requirements.txt`
```
pip install -r requirements.txt
```
4. Execute `first_run.py` to get the latest status id
```bash
python3 first_run.py
```

### Obtain Mastadon Developer Access Token
1. Navigate to your Mastadon instance > Settings > Development
2. Click on **New Application** and enter below fields:
- Application Name: *Can be anything*
- Application Website: *Leave it blank*
- Scopes: read: statuses *(minimally)*
3. Click **Submit**
4. Click on your newly created application
5. Copy your access token. This token will be added to your `config.py` **access_token**

### Obtain IFTTT webhook key and IFTTT event name
1. Navigate to [IFTTT](https://ifttt.com) and create a account if no account exist yet.
2. Navigate to [IFTTT Webhook](https://ifttt.com/maker_webhooks) and click **Documentation**
3. Copy the key shown on the page. This key will be added to your `config.py` **ifttt_webhook_key**
4. Navigate back to [IFTTT](https://ifttt.com) and create a new applet.
5. Beside the text **If this**, click **add**
6. Search for **Webhooks** and click on it
7. Click **Receive a web request**
8. Enter any name for event name. This value will be added to your `config.py` **ifttt_event**. Click **Update trigger**
9. Beside **Then That**, click **Add**
10. Search for **Day One**. Click on Create Journal Entry
11. Authenticate with Day One if prompted. Select your Day One account and journal which you want to create the posts in.
12. For body, remove everything except **Value1**. You can use *Add ingredient** to add Value1 if you removed all contents in body accidentally.
13. Add in your tags (optional)
14. Remnove everything from Latitude, Longitude and Place Name since it will be empty.
15. Click Create action


## Running the script
Execute `app.py`
```
python3 app.py
```

## Information
- Script look for new posts every 60 seconds
- There is a delay of 12 seconds for each webhook requests due to IFTTT internal 10 seconds cooldown + 2 seconds for buffer.