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

if __name__ == '__main__':
  print('Getting Driver')
  driver = get_driver()

  print('Fetching Trending Videos')

  video_divs = get_videos(driver)
  print(f'Found {len(video_divs)} trending videos.')

