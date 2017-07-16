import requests
from bs4 import BeautifulSoup

link="https://thepiratebay.org/torrent/18104506/"

r=requests.get(link)
soup=BeautifulSoup(r.content)
for i in soup.findAll("a",{"style":"background-image: url('//thepiratebay.org/static/img/icons/icon-magnet.gif');"}):
		print i.get('href')

