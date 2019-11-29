from selenium import webdriver
import time
import csv
import json

class YoutubeScraper:
	#Constructor with URL of playlist
	def __init__(self):
		self.driver = webdriver.Chrome()
	#Making assumption that the link points to a valid playlist
	def openPlaylist(self,url_link):
		self.driver.get(url_link)
		#Store the name of the playlist
		self.playlistName = self.driver.find_element_by_xpath('//*[@id="title"]').text
		self.playlistName = self.playlistName.replace(' ','').replace('/','').replace('|','').replace('\'','').replace('\"','')

	#Scrape and create JSONs with infinite scroll
	def scrape_infiniteScroll(self,pauseTime, repeatScroll):
		for i in range(1,repeatScroll):
			self.driver.execute_script("window.scrollTo(0,100800);")
			time.sleep(pauseTime)

		self.video_elements = self.driver.find_elements_by_tag_name('ytd-playlist-video-renderer')
	#Play songs in the JSON
	def play_shuffledSongs(self):
		play_button = self.driver.find_element_by_xpath('//*[@aria-label="Shuffle play"]')
		play_button.click()
	#Parse WebElements remove the private and deleted videos, 
	#and store relevant information in a list
	def create_metadataList(self):
		self.videosList = []
		for element in self.video_elements:
			data = element.text.split('\n')
			if(len(data)>2):
				video_url = element.find_element_by_xpath(".//a[@href]").get_attribute("href")
				json_dict = dict(zip(['Name','Channel','Link','PlaylistName'],[data[-2],data[-1],video_url,self.playlistName]))
				self.videosList.append(json_dict)

	#Create JSONDump
	def create_JsonDump(self,fileName):
		with open(fileName,'w') as json_file:
			json_file.write('[')
			for video in self.videosList[:-1]:
				json.dump(video,json_file)
				json_file.write(',')
			json.dump(self.videosList[-1],json_file)
			json_file.write(']')

	def close_driver(self):
		self.driver.close()

class ChatbotAssist():
	def __init__(self):
		self.myScraper = YoutubeScraper()
		self.list_Playlists = []

	#Gets Playlist urls and stores them in a list of tuples {name,URL}
	def fetch_playlistUrls(self):
		with open('RawData/urlsToPlayList.txt','r') as urlsFile:
			for line in urlsFile:
				playlist_link = line.replace('\n','')
				self.myScraper.openPlaylist(playlist_link)
				self.list_Playlists.append((self.myScraper.playlistName,playlist_link))
		# return self.list_Playlists
	# Create Json files for each playlist
	def create_jsonFiles(self):
		if not self.list_Playlists:
			self.fetch_playlistUrls()
		for item in self.list_Playlists:
			self.myScraper.openPlaylist(item[1])
			self.myScraper.scrape_infiniteScroll(2,10)
			self.myScraper.create_metadataList()
			self.myScraper.create_JsonDump('RawData/jsonDumps/'+item[0]+'.txt')
