import os
import json
import smtplib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

Youtube_trending_url = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def get_videos(driver):
  driver.get(Youtube_trending_url)
  VIDEO_DIV_TAG = 'ytd-video-renderer'
  videos = driver.find_elements(By.TAG_NAME,VIDEO_DIV_TAG)
  return videos

def parse_video(video):

  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text
  url = title_tag.get_attribute('href')

  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail_url = thumbnail_tag.get_attribute('src')

  channel_tag = video.find_element(By.CLASS_NAME,'ytd-channel-name')
  channel_name = channel_tag.text

  description_tag = video.find_element(By.ID, 'description-text').text

  return {
    'title':title,
    'url':url,
    'thubmnail':thumbnail_url,
    'channel_name':channel_name,
    'description':description_tag
  }

def send_mail(body):
  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()   # optional
    
    SENDER_EMAIL = 'trensetterforyou@gmail.com'
    RECIEVER_EMAIL = ['iitbtanuj@gmail.com','194113@nith.ac.in']
    SENDER_PASSWORD = os.environ['GMAIL_PASSWORD']
  
    subject = 'Test Message from REPLit'

    email_text = f'''\
    From: {SENDER_EMAIL}
    To: {RECIEVER_EMAIL}
    Subject: {subject}

    {body}
    '''
    print(email_text)
    server_ssl.login(SENDER_EMAIL,SENDER_PASSWORD)
    server_ssl.sendmail(SENDER_EMAIL, RECIEVER_EMAIL, email_text)
    server_ssl.close() 
    print('Mail Sent')
  except:
      print('Something went wrong...')

if __name__ == '__main__':
  print('Getting Driver')
  driver = get_driver()

  print('Fetching Trending Videos')

  videos = get_videos(driver)
  print(f'Found {len(videos)} trending videos.')

  # title, url, channel, views, time uploaded, dicription, thumbnail url

  print('Parsing Top 10 Videos.')
  videos_data = [parse_video(video) for video in videos[:10]]
  
  print('Saving The Data To A CSV File.')

  videos_df = pd.DataFrame(videos_data)
  #print(videos_df)

  videos_df.to_csv('Trending.csv',index=None)

  print('send the result over email.')
  body = json.dumps(videos_data,indent=2)
  send_mail(body)

  print('Finished.')