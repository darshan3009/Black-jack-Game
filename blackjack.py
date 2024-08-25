from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
import random
import database


class blackjackUI(QWidget):
	def __init__(self,username):
		super(blackjackUI,self).__init__()
		self.userdata = database.get_user_info(username)

		#load the ui file
		uic.loadUi("UI/blackjack.ui",self)
		# self.setFixedSize(900,650)
		#Define out widgets
		self.dealercard1=self.findChild(QLabel,"dealercard1")
		self.dealercard2=self.findChild(QLabel,"dealercard2")
		self.dealercard3=self.findChild(QLabel,"dealercard3")
		self.dealercard4=self.findChild(QLabel,"dealercard4")
		self.dealercard5=self.findChild(QLabel,"dealercard5")
		
		self.playercard1=self.findChild(QLabel,"playercard1")
		self.playercard2=self.findChild(QLabel,"playercard2")
		self.playercard3=self.findChild(QLabel,"playercard3")
		self.playercard4=self.findChild(QLabel,"playercard4")
		self.playercard5=self.findChild(QLabel,"playercard5")
		
		self.dealerHeaderLabel=self.findChild(QLabel,"dlabel")
		self.playerHeaderLabel=self.findChild(QLabel,"plabel")
		
		self.shuffelButton=self.findChild(QPushButton,"spushbutton")
		self.hitMeButton=self.findChild(QPushButton,"hitme")
		self.standButton=self.findChild(QPushButton,"stand")
		self.balanceL = self.findChild(QLabel,'stats')
		self.plabel = self.findChild(QLabel,'plabel')
		
		#Shuffel card
		self.shuffle()

		#click buttons
		self.shuffelButton.clicked.connect(self.shuffle)
		self.hitMeButton.clicked.connect(self.playerHit)
		self.standButton.clicked.connect(self.pressStand)
		self.plabel.setText(f"{username}")
		self.plabel.adjustSize()
		self.setstats()
		
		#Show the app
		self.show()
	#check for blackjack

	def setstats(self):
		self.userdata = database.get_user_info(self.userdata[0])
		self.balanceL.setText(f'Balance: {self.userdata[2]}\nPlayed: {self.userdata[3]}\nWin: {self.userdata[4]}\nLoss: {self.userdata[5]}')



	def pressStand(self):
		#Disable buttons
		self.standButton.setEnabled(False)
		self.hitMeButton.setEnabled(False)
		
		self.player_total=0
		self.dealer_total=0
	
		#get the player score
		for score in self.player_score:
			self.player_total+=score
	
		#get the player score
		for score in self.dealer_score:
			self.dealer_total+=score
		
		#logic
		if self.dealer_total>=17:
			#check for bust
			if self.dealer_total>21:
				#check for bust
				QMessageBox.about(self,"	Player Wins	",f" Player Wins ! Dealer Has : {self.dealer_total} Player Has : {self.player_total}")
				database.game_won(self.userdata[0])
				self.setstats()
			elif self.dealer_total==self.player_total:
				#tie
				QMessageBox.about(self,"	Tie !!	",f" It's a tie !! Dealer Has : {self.dealer_total} Player Has : {self.player_total}")
				database.game_tie(self.userdata[0])
				self.setstats()
			elif self.dealer_total>self.player_total:
				#dealer wins
				QMessageBox.about(self,"	Dealer Wins	",f" Dealer Wins ! Dealer Has : {self.dealer_total} Player Has : {self.player_total}")	
				database.game_loss(self.userdata[0])
				self.setstats()
			else:
				#player wins
				QMessageBox.about(self,"	Player Wins	",f" Player Wins! Dealer Has : {self.dealer_total} Player Has : {self.player_total}")
				database.game_won(self.userdata[0])
				self.setstats()
		else:
		#Dealer needs another card!
			self.dealerHit()
			self.pressStand()
		
	def blackjack_check(self,player):
		
		self.player_total=0
		self.dealer_total=0
	
		
		if player == "dealer":
			if len(self.dealer_score)==2:
				if self.dealer_score[0]+self.dealer_score[1]==21:
					#change blackjack status to yes
					self.blackjack_status["dealer"]="yes"
							
		if player == "player":
			if len(self.player_score)==2:
				if self.player_score[0]+self.player_score[1]==21:
					#change blackjack status to yes
					self.blackjack_status["player"]="yes"
			else:
				#loop through player score list and add up cards
				for score in self.player_score:
					self.player_total+=score
					
				if self.player_total==21:
					self.blackjack_status["player"]="yes"
				elif self.player_total>21:
					#check for ace
					for card_num,card in enumerate(self.player_score):
						#change 11 to 1
						if card==11:
							self.player_score[card_num]=1
							
							#update player totals
							self.player_total=0
							
							for score in self.player_score:
								#add up score
								self.player_total+=score
							
							#check for bust
							if self.player_total>21:
								self.blackjack_status["player"]="bust"
							
					else:
						#check for win or bust
						if self.player_total==21:
							self.blackjack_status["player"]="yes"
				
						if self.player_total>21:
							self.blackjack_status["player"]="bust"
					
							
						
		#check for blackjack
		if	len(self.player_score)==2 and len(self.dealer_score)==2:
			#check for tie
			if self.blackjack_status["dealer"]=="yes" and self.blackjack_status["player"]=="yes":
				#winner message
				QMessageBox.about(self, "	Push !!	", "	It's a tie !!	")
				database.game_tie(self.userdata[0])
				self.setstats()
				#Disable buttons
				self.hitMeButton.setEnabled(False)
				self.standButton.setEnabled(False)
	
			elif self.blackjack_status["dealer"]=="yes" :
				#winner message
				QMessageBox.about(self, "	Blackjack !!	", "	Dealer Wins !!	")
				database.game_loss(self.userdata[0])
				self.setstats()
				#Disable buttons
				self.hitMeButton.setEnabled(False)
				self.standButton.setEnabled(False)
			
			elif self.blackjack_status["player"]=="yes" :
				#winner message
				QMessageBox.about(self, "	Blackjack !!	", "	Player Wins !!	")
				database.game_won(self.userdata[0])
				self.setstats()
				#Disable buttons
				self.hitMeButton.setEnabled(False)
				self.standButton.setEnabled(False)
		else:
			if self.blackjack_status["dealer"]=="yes" and self.blackjack_status["player"]=="yes":
				#winner message
				QMessageBox.about(self, "	Push !!	", "	It's a tie !!	")
				database.game_tie(self.userdata[0])
				self.setstats()
				#Disable buttons
				self.hitMeButton.setEnabled(False)
				self.standButton.setEnabled(False)
	
			elif self.blackjack_status["dealer"]=="yes":
				#winner message
				QMessageBox.about(self, "	Dealer  Wins !!	", "	21 Dealer Wins !!	")
				database.game_loss(self.userdata[0])
				self.setstats()
				#Disable buttons
				self.hitMeButton.setEnabled(False)
				self.standButton.setEnabled(False)
			
			elif self.blackjack_status["player"]=="yes" and self.blackjack_status["dealer"]=="no" :
				#winner message
				QMessageBox.about(self, "	Player Wins !!	", "	21 Player Wins !!	")
				database.game_won(self.userdata[0])
				self.setstats()
				#Disable buttons
				self.hitMeButton.setEnabled(False)
				self.standButton.setEnabled(False)
		
		if self.blackjack_status["player"]=="bust":
			#bust message
			QMessageBox.about(self, "	Bust !!	", f" Player Loses : {self.player_total}	")
			database.game_loss(self.userdata[0])
			self.setstats()
			self.hitMeButton.setEnabled(False)
			self.standButton.setEnabled(False)
		
				
	def shuffle(self):
		
		#keep track of score totals
		
		self.player_total=0
		self.dealer_total=0
				
		#create dictniory to keep track of blackjack status
		self.blackjack_status={"dealer":"no","player":"no"}
		#Enable buttons
		self.hitMeButton.setEnabled(True)
		self.standButton.setEnabled(True)
		
		#Reset card images
		pixmap = QPixmap('image/back.png')
		self.dealercard1.setPixmap(pixmap)
		self.dealercard2.setPixmap(pixmap)
		self.dealercard3.setPixmap(pixmap)
		self.dealercard4.setPixmap(pixmap)
		self.dealercard5.setPixmap(pixmap)
		
		self.playercard1.setPixmap(pixmap)
		self.playercard2.setPixmap(pixmap)
		self.playercard3.setPixmap(pixmap)
		self.playercard4.setPixmap(pixmap)
		self.playercard5.setPixmap(pixmap)              
		#Define our Deck
		suits=["diamonds","club","hearts","spade"]
		values=range(2,15)
		
		#Create Deck
		
		#global deck
		self.deck=[]
		
		for suit in suits:
			for value in values:
				self.deck.append(f"{value}_of_{suit}")
				
		#create Our Players		
		#global dealer,player
			 
		self.dealer=[]
		self.player=[]
		self.dealer_score=[]
		self.player_score=[]
		self.playerSpot=0
		self.dealerSpot=0
		
		self.dealerHit()	
		self.dealerHit()	
		
		self.playerHit()
		self.playerHit()
	
	def dealCards(self):
		try:#Grab a random card from Dealer
			card=random.choice(self.deck)
			
			#Add the card to the dealer's list
			self.dealer.append(card)
			
			#Remove the card from the deck
			self.deck.remove(card)
				
			#Output Card To screen
			pixmap=QPixmap(f'image/{card}.png')
			self.dealercard1.setPixmap(pixmap)
				
			#Grab a random card from Player
			card=random.choice(self.deck)
			
			#Add the card to the player's list
			self.player.append(card)
			
			#Remove the card from the deck
			self.deck.remove(card)
				
			#Output Card To screen
			pixmap=QPixmap(f'image/{card}.png')
			self.playercard1.setPixmap(pixmap)
				
			self.setWindowTitle(f"{len(self.deck)} Cards Left In Deck... ")
		except:
			self.setWindowTitle("Game Over")
	
	def dealerHit(self):
		if self.playerSpot <= 5:
		#	print("inside player hit",self.playerSpot)
			try:
				#Grab a random card from Player
				card=random.choice(self.deck)
	
				#Remove the card from the deck
				self.deck.remove(card)
				
				#Add the card to the player's list
				self.dealer.append(card)
				
				#Add card to dealer score
				self.dcard=int(card.split("_",1)[0])
				if self.dcard == 14:
					self.dealer_score.append(11)
				elif self.dcard == 11 or self.dcard == 12 or self.dcard == 13:	
					self.dealer_score.append(10)
				else:
					self.dealer_score.append(self.dcard)
					
					
				#Output Card To screen
				pixmap=QPixmap(f'image/{card}.png')
				
				if self.dealerSpot == 0:
					self.dealercard1.setPixmap(pixmap)
					self.dealerSpot += 1 
				
				elif self.dealerSpot == 1:
					self.dealercard2.setPixmap(pixmap)
					self.dealerSpot += 1 
				
				elif self.dealerSpot == 2:
					self.dealercard3.setPixmap(pixmap)
					self.dealerSpot +=1
								
				elif self.dealerSpot == 3:
					self.dealercard4.setPixmap(pixmap)
					self.dealerSpot +=1
				
				elif self.dealerSpot == 4:
					self.dealercard5 .setPixmap(pixmap)
					self.dealerSpot +=1
					
				self.setWindowTitle(f"{len(self.deck)} Cards Left In Deck... ")
			except:
				self.setWindowTitle("Game Over")
			
			self.blackjack_check("dealer")

	def playerHit(self):
		if self.playerSpot <= 5:
			try:
				#Grab a random card from Player
				card=random.choice(self.deck)
	
				#Remove the card from the deck
				self.deck.remove(card)
				
				#Add the card to the player's list
				self.player.append(card)
				
				self.pcard=int(card.split("_",1)[0])
				self.player_score.append(self.pcard)
				# if self.pcard == 14:
				# 	self.player_score.append(11)
				# elif self.pcard == 11 or self.pcard == 12 or self.pcard == 13:	
				# 	self.player_score.append(10)
				# else:
				
					
				#Output Card To screen
				pixmap=QPixmap(f'image/{card}.png')
				
				if self.playerSpot == 0:
					self.playercard1.setPixmap(pixmap)
					self.playerSpot += 1 
				
				elif self.playerSpot == 1:
					self.playercard2.setPixmap(pixmap)
					self.playerSpot += 1 
				
				elif self.playerSpot == 2:
					self.playercard3.setPixmap(pixmap)
					self.playerSpot +=1
								
				elif self.playerSpot == 3:
					self.playercard4.setPixmap(pixmap)
					self.playerSpot +=1
				
				elif self.playerSpot == 4:
					self.playercard5 .setPixmap(pixmap)
					self.playerSpot +=1
					
				self.setWindowTitle(f"{len(self.deck)} Cards Left In Deck... ")
			except:
				self.setWindowTitle("Game Over")
			
			#check for blackjack
			self.blackjack_check("player")
