import requests 
import bs4 as bs 
import pandas as pd 
import io

url = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"

base = requests.get(url)
soup = bs.BeautifulSoup(base.text, 'lxml')
links = soup.find('tbody').find_all('a')

raw_base = 'https://raw.githubusercontent.com'

csv_files = []
for link in links:
    if link.get('href').endswith('.csv'):
        # csv file 
        tail = link.get('href')
        tail = tail.split('/')
        tail.pop(3)
        tail = '/'.join(tail)
        dl_url = raw_base + tail
        csv_files.append(dl_url)

df = pd.DataFrame()

for i,cf in enumerate(csv_files):

    data = requests.get(cf)
    data = data.content
    df = df.append(pd.read_csv(io.BytesIO(data)))

df.to_csv('covid19.csv', index=False)