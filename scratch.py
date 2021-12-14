import requests
from bs4 import BeautifulSoup

Youtube_trending_url = 'https://www.youtube.com/feed/trending'

# doesn't execute javascript
response = requests.get(Youtube_trending_url)

print('Status Code', response.status_code)
# print('Outuput', response.text[:1000])

with open('trending.html', 'w') as f:
  f.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')

print('Page title:', doc.title.text)

# find all video divs
video_divs = doc.find_all('div', class_ = 'ytd-video-renderer')
print(f'Found {len(video_divs)} videos')