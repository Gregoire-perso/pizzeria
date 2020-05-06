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
>>> display_budget(self, curses_screen constant_scr) --> "constant_scr --> screen of money, days, level, ..."
	 display player budget		
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
			self.oven_level = 1;

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
	
	#===========================================================

	def credit(self, how_much, constant_scr):
		"""Check if the credit is correct
		Return True if it is, else return False """
		if(how_much > 0):
			if self.money + how_much >= 0:
				self.money += how_much;
				self.display_budget(constant_scr);
				return(True);
	
		return(False);

	#===========================================================

	def debit(self, how_much, constant_scr):
		if(how_much > 0):
			if (self.money - how_much) >= 0:
				self.money -= how_much;
				self.display_budget(constant_scr);
				return(True);

		return(False);
	
	#===========================================================

	def display_budget(self, const_scr):
		const_scr.addstr(1, 1, "Jour numéro {0}".format(self.days));
		const_scr.addstr(2, 1, "{0} : {1}".format(emoji.emojize(":euro_banknote:"), self.money));
		const_scr.refresh();

	#===========================================================
	
	def do_price_list(self, ingredients_buying_price_list):
		price_list = [];
		for i, j in ingredients_buying_price_list:
			if (i in self.ingredients.keys()):
				price_list.append("   Déjà acheté   ");

			else:
				len_price = len(str(j)) + 1;
				temp = " " * ((17 - len_price) // 2);
				temp += str(j) + "€";
				temp += " " * (17 - len(temp));
				price_list.append(temp);
		return (price_list);
	
	#===========================================================

	def upgrade_menu(self, main_scr, const_scr):
		main_scr.clear();
		main_scr.addstr(2, 2, "Que voulez-vous faire ?");
		main_scr.addstr(3, 4, "1 : Acheter de nouveaux ingrédients");
		main_scr.addstr(4, 4, "2 : Améliorer votre four");

		key = main_scr.getkey();

		while (key not in '12'):
			key = main_scr.getkey();

		if (key == '1'):
			self.upgrade_ingredient(main_scr, const_scr);
		
		else:
			self.upgrade_equipment(main_scr, const_scr);

	#===========================================================
	
	def upgrade_ingredient(self, main_scr, const_scr):
		main_scr.clear();
		with open("../packages/ingredients_buying_price.json", "r") as f:
			ingredients_buying_price = json.load(f);

		with open("../languages/french/connection_emoji_ingredient.json", "r") as f:
			connection_emoji_ingredient = json.load(f);

		emoji_list = ["        " + emoji.emojize(":"+i+":") + "       " for i in ingredients_buying_price.keys()];
		
		ingredient_name_list = [];
		k = 1;
		for i in ingredients_buying_price.keys():
			name = connection_emoji_ingredient[i];
			temp = " " * ((17 - len(name)) // 2 - 1);
			temp += str(k) + ": " + name;
			temp += " " * (17 - len(temp));
			ingredient_name_list.append(temp);
			k += 1;

		ingredients_buying_price_list = list(ingredients_buying_price.items());
		
		key = 'e';
		scr_number = 0; #Screen number for the ingredients
		price_list = self.do_price_list(ingredients_buying_price_list);
		while (key != 'q'):
			temp = "{"+str(0+scr_number)+"}|{"+str(1+scr_number)+"}|{"+str(2+scr_number)+"}|{"+str(3+scr_number)+"}";
			main_scr.addstr(2, 2, "   " + temp.format(*emoji_list) + "   ");
			main_scr.addstr(3, 2, "<--" + temp.format(*ingredient_name_list) + "-->");
			main_scr.addstr(4, 2, "   " + temp.format(*price_list) + "   ");
			main_scr.addstr(5, 2, "Appuyez sur le numéro de l'ingrédient que vous voulez acheter, \nou 'q' pour quitter");
			main_scr.refresh();
			key = main_scr.getkey().lower();

			if (key == 'key_right'):
				scr_number = scr_number + 4 if scr_number + 7 < len(emoji_list)-1 else len(emoji_list) - 4;

			elif (key == 'key_left'):
				scr_number = scr_number - 4 if scr_number - 4 > 0 else 0;

			elif (key == 'q'):
				break;

			else:
				with open("../packages/all_ingredients.json", "r") as f:
					temp = json.load(f);
		
				if (self.debit(ingredients_buying_price_list[int(key)-1][1], const_scr)):
					self.ingredients[ingredients_buying_price_list[int(key)-1][0]] = temp[ingredients_buying_price_list[int(key)-1][0]];
					price_list = self.do_price_list(ingredients_buying_price_list);

		main_scr.clear();
		main_scr.refresh();
	
	#===========================================================

	def upgrade_equipment(self, main_scr, const_scr):
		main_scr.clear();
		key = 'e';

		while (key != 'q'):
			main_scr.addstr(2, 2, "Équipement : Four");
			main_scr.addstr(3, 2, "Niveau : " + str(self.oven_level));
			main_scr.addstr(4, 2, "Temps de cuisson : " + str(self.cooking_time) + " secondes");
			main_scr.addstr(5, 2, "Gain de l'amélioration : 0.2 secondes");
			main_scr.addstr(6, 2, "Prix : 100€");
			main_scr.addstr(7, 2, "Appuyez sur 1 pour améliorer, ou 'q' pour quitter");
			main_scr.refresh();

			key = main_scr.getkey().lower();
			
			if (key == '1'):
				if (self.debit(100, const_scr)):
					self.oven_level += 1;
					self.cooking_time = round(self.cooking_time - 0.2, 2);

		main_scr.clear();
		main_scr.refresh();
			

