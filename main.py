import kivy, threading, time
kivy.require("1.9.0")
base_url='https://torrentz2.eu'
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from torrent import get_search,down_magnet
from functools import partial

adult=True
s_res={}
tl=""

class Home(Screen):
	global adult
	def __init__(self, **kwargs):
		super(Home, self).__init__(**kwargs)


	def serch(self,q):
		b=Button(text='Searching',background_color=(0.2,0.6,1,0.1))
		self.popup=Popup(title=q,content=b,size_hint=(1,1),size=(150,150))
		self.popup.open()
		self.search_thread=threading.Thread(target=self.search,args=(q,))
		self.search_thread.start()
		serch_anim_thread=threading.Thread(target=self.serch_anim,args=())
		serch_anim_thread.start()
	 
	def serch_anim(self):
		while self.search_thread.is_alive():
			self.popup.content.background_color[3]+=.1
			if(self.popup.content.background_color[3]>=1):
				self.popup.content.background_color[3]=0.1
			time.sleep(.05)

	def search(self,q):
		global adult
		global s_res
		s_res,titles=get_search(adult,q)
		if(titles[0]=='Error'):
			popup=Popup(title='Error',content=Label(text='Please Check your INTERNET'),size_hint=(None,None),size=(300,150))
			popup.open()
		else:
			stack=self.ids['res_stack']
			stack.clear_widgets()
			for nam in titles:
				b=Button(text=nam,size_hint=[1,None],height=60,font_size=18)
				bcb=partial(self.detail,nam)
				b.bind(on_release=bcb)
				stack.add_widget(b)

		self.popup.dismiss()


	def detail(self,ttl,instance):
		global tl
		tl=ttl
		self.manager.current='details_name'


class Settings(Screen):
	def __init__(self, **kwargs):
		super(Settings, self).__init__(**kwargs)

	def switch(self, instance, value):
		global adult
		if value is True:
			adult=True
		else:
			adult=False


class Details(Screen):
	def __init__(self, **kwargs):
		super(Details, self).__init__(**kwargs)

	def on_pre_enter(self):
		global tl
		global s_res
		self.ids.ttl_lbl.text=tl
		self.ids.link_input.text=base_url+s_res[tl][0]
		self.ids.size.text=s_res[tl][1]
		self.ids.peers.text=s_res[tl][2]
		self.ids.seeds.text=s_res[tl][3]


	def open_magnet(self):
		b=Button(text='Starting Download',background_color=(0.2,0.6,1,0.1))
		self.popup=Popup(title='',content=b,size_hint=(1,1),size=(150,150))
		self.popup.open()
		self.magnet_thread=threading.Thread(target=self.search_magnet,args=())
		self.magnet_thread.start()
		serch_anim_thread=threading.Thread(target=self.down_anim,args=())
		serch_anim_thread.start()


	def down_anim(self):
		while self.magnet_thread.is_alive():
			self.popup.content.background_color[3]+=.1
			if(self.popup.content.background_color[3]>=1):
				self.popup.content.background_color[3]=0.1
			time.sleep(.05)


	def search_magnet(self):
		global tl
		global s_res
		link=base_url+s_res[tl][0]
		chk=down_magnet(link)
		self.popup.dismiss()
		try:	
			popup = Popup(title=chk['title'],content=Label(text=chk['msg']),size_hint=(None, None), size=(300, 150))
			popup.open()
		except:
			pass


class MyManager(ScreenManager):
	def __init__(self, **kwargs):
		super(MyManager, self).__init__(**kwargs)
		self.add_widget(Home(name="home_name",))
		self.add_widget(Settings(name="settings_name",))
		self.add_widget(Details(name="details_name",))
		self.transition=FadeTransition()
		self.transition.duration=.18
		self.current='home_name'

	

class TorrentApp(App):
	def build(self):
		return MyManager()
   
               
if __name__=="__main__":
    app=TorrentApp()
    app.run()