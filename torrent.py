import requests, os
from bs4 import BeautifulSoup
base_url='https://torrentz2.eu'

def get_search(adult, q):
	global base_url
	if adult is True:
		q_url=base_url+'/search?f='+q
	else:
		q_url=base_url+'/search?f='+q+'&safe=1'

	try:
		r=requests.get(q_url)
	except:
		return {"Error":['','','','']},["Error"]

	soup=BeautifulSoup(r.content,'lxml')

	data=dict()
	titles=list()
	for dat in soup.find_all('dl'):
		if len(list(list(dat.children)[1].children))>4 and len(data.keys())<30:
			link=list(list(dat.children)[0].children)[0].get('href')
			names=list(dat.children)[0].text
			size=list(list(dat.children)[1].children)[2].text
			peers=list(list(dat.children)[1].children)[3].text
			seeds=list(list(dat.children)[1].children)[4].text
			res=[link,size,peers,seeds]
			data[names]=res
			titles.append(names)

	if not len(data.keys()):
		return {"No Result":["","","",""]},["No Result"]
	return data,titles


def down_magnet(link):
	try:
		r=requests.get(link)
	except:
		return {"title":"Error","msg":"Check Your Internet"}

	soup=BeautifulSoup(r.content,'lxml')
	down_links=dict()
	for sites in soup.find_all('span'):
		if(sites.get('class')==['u']):
			if(sites.text.strip()=='monova.org'):
				down_links['monova.org']=sites.parent.get('href')
			if(sites.text.strip()=='thepiratebay.se'):
				down_links['thepiratebay.se']=sites.parent.get('href')
			
	try:
		magnet=from_monova(down_links['monova.org'])
	except:
		try:
			magnet=from_piratebay(down_links['thepiratebay.se'])
		except:
			return {"title":"Try Again","msg":"Try Again"}

	try:
		os.system("qbittorrent %s"%(magnet))
	except:
		return {"title":"Error","msg":"Please Install qbittorrent"}

	return {"title":"Download","msg":"Downloading Started"}



def from_monova(link):
	try:
		r=requests.get(link)
	except:
		return {"title":"Error","msg":"Check Your Internet"}
	soup=BeautifulSoup(r.content,'lxml')
	for i in soup.findAll("a",{"id":"download-file"}):
		return i.get('href')
	

def from_piratebay(link):
	try:
		r=requests.get(link)
	except:
		return {"title":"Error","msg":"Check Your Internet"}
	soup=BeautifulSoup(r.content,'lxml')
	for i in soup.findAll("a",{"style":"background-image: url('//thepiratebay.org/static/img/icons/icon-magnet.gif');"}):
		return i.get('href')