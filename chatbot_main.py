import os
import spacy
from crawler import ChatbotAssist
#List of Commads
'''
What are my options
Show my playlists

'''

class chatBot:
	def __init__(self,chatbot_Name):
		self.name = chatbot_Name
		dummy_variable = os.system('clear')
		self.nlp = spacy.load('en_core_web_sm')
		self.ytassist = ChatbotAssist()

	def chatbotManager(self):
		return input('>>Im ' + self.name + '. How can I help with choosing your music?\n>>')

	#This function parses the command, and the returns only the essential words
	def parse_command(self,input_command):
		tokens = self.nlp(input_command)
		tokens = self.nlp(' '.join([token.lemma_ for token in tokens]))
		output_cmd = ' '.join([token.text for token in tokens if (token.tag_ == 'VB' or token.tag_ =='NN')])
		return output_cmd
		
	def list_playlists(self):
		print("Here's all your music playlists:\n")
		if not self.ytassist.list_playlists:
			self.list_playlists = self.ytassist.fetch_playlistUrls()
		for i in range(len(self.list_playlists)):
			print(i,'. ', self.list_playlists[i][0])

	def run_chatbot(self):
		flag = True
		while(flag):
			answer = self.chatbotManager()
			answer = self.parse_command(answer)

if __name__ == '__main__':
	bot = chatBot('Bubblegumbob')
	# Create Jsons for each of the playlists
	bot.ytassist.create_jsonFiles()
	# bot.run_chatbot()
	# bot.list_playlists()