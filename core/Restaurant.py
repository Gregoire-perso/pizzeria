# Restaurant manage file
"""
Restaurant documentation

Properties: 
>>> list ingredients --> "unlocked ingredients"
>>> int cooking_time --> "time of waiting for cooking a pizza"
>>> dict connecion_key_ingredient --> "connections between a key and an ingredient (only for the computer)"
>>> dict connection_key_ingredient_display --> "same as before but for displaying on the screen" 
>>> str name --> "name of the player"
>>> str surname --> "surname of the player"
>>> int xp --> "total xp number"
>>> int level --> "level of the restaurant"
>>> float money --> "money left for the player"
>>> int days --> "number of days passed since the start of the game"
>>> int rent --> "rent for a day"

Methods:
>>> __init__(self, str name, str surname) --> "name --> name of the player, surname --> surname of the player"
	 constructor of the restaurant
>>> credit(self, float how_much, curses_screen constant_scr) --> "how_much --> how much credit, constant_scr --> screen of money, days, level, ..."
	 credit "how much" to the money of the player
>>> debit(self, float how_much, curses_screen constant_scr) --> "same as previous line"
	 debit "how_much" of to money of the player
>>> display_const(self, curses_screen constant_scr) --> "constant_scr --> screen of money, days, level, ..."
	 display constant game like level, days, money left		
"""
# Global import
import json;
import curses;
import emoji;

class Restaurant:
	def __init__(self, name, surname):
		with open("../packages/default_ingredients.json", "r") as f:
			self.ingredients = json.load(f);

		with open("../packages/default_cooking_time.txt", "r") as f:
			self.cooking_time = int(f.read().replace("\n", ""));

		with open("../packages/default_connection_key_ingredient.json", "r") as f:
			self.connection_key_ingredient = json.load(f); # {'key': 'emoji_code_of_ingredient', ...}

		with open("../languages/french/default_connection_key_ingredient_display.json", "r") as f:
			self.connection_key_ingredient_display = json.load(f); # {'key': 'name_of_ingredient', ...}
			
		self.name = name;
		self.surname = surname;
		self._xp = 1;
		self._level = 1;
		self._money = 50;
		self.days = 1;
		self.rent = 10;


	@property
	def xp(self):
		return(self._xp);

	@xp.setter
	def xp(self, new_xp):
		self._xp = new_xp;
		
		if self._xp - 75*2**(self._level+1) > 0:
			self._level += 1;

	@property
	def money(self):
		return(self._money);
	
	@money.setter
	def money(self, new_money):
		self._money = new_money;

	def credit(self, how_much, constant_scr):
		"""Check if the credit is correct
		Return True if it is, else return False """
		if(how_much > 0):
			if self.money + how_much >= 0:
				self.money += how_much;
				self.display_const(constant_scr);
				return(True);
	
		return(False);

	def debit(self, how_much, constant_scr):
		if(how_much > 0):
			if (self.money - how_much) >= 0:
				self.money -= how_much;
				self.display_const(constant_scr);
				return(True);

		return(False);

	def display_const(self, constant_scr):
		constant_scr.clear();
		constant_scr.addstr(0, 0, "Jour numéro {0}".format(self.days));
		constant_scr.addstr(1, 0, "{0} : {1}".format(emoji.emojize(":dollar_banknote:"), self.money));
		constant_scr.refresh();

