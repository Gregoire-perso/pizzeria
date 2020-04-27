# Pizza file
"""
Pizza documentation

Properties: 
>>> Client client : "Client object that command the pizza"
>>> window scr : "Main screen (where the pizza is cooked)"
>>> window constant_scr : "Screen that show money left, number of the day, level, ..."
>>> Restaurant restaurant : "Restaurant object (the player)"
>>> list ingredient_wanted : "List of wanted ingredients"
>>> dict ingredients_on_pizza : "Dict of ingredients currently on the pizza ({ingredient_name: number_of_that})"
>>> list ingredients_coordinates : "List of coordinates of every ingredient ([[x, y], [x, y], ...])"
>>> int x : "x of the cursor"
>>> int y : "y of the cursor"
>>> bool cooked : "if the pizza is cooked or not"
>>> int outgoings_expense : "sum of outgoings expense"

Methods: 
>>> __init__(self, Client client, Restaurant restaurant, list ingredient_wanted, window scr, window constant_scr) : "same as properties"
	constructor of the pizza
>>> do_pizza(self)
	do what is needed to cook the pizza
>>> display_pizza(self, int color_pair) : "color_pair: number of which color pair for displaying"
	display the pizza
>>> correct_position(self)
	check if the player can add an ingredient at the current position
>>> overdraft(self, str ingredient) : "ingredient: name of the ingredient that is added"
	check if the player have enough money and debit the player if that's the case
>>> put_ingredients(self)
	method that recover key that are entered, move the cursor and serve the client at the end
>>> add_ingredient(self, str which_one) : "which_one: ingredient that whants to be added"
	add the ingredient if it can be
>>> cook(self)
	cook the pizza
"""
# Global import
import curses;
import time;
import math;
import emoji;

class Pizza:
	def __init__(self, client, restaurant, ingredient_wanted, scr, constant_scr):
		self.client = client;
		self.scr = scr;
		self.constant_scr = constant_scr;
		self.restaurant = restaurant;
		self.restaurant.display_const(self.constant_scr);
		self.ingredient_wanted = ingredient_wanted;
		self.ingredients_on_pizza = {}; # dict : {ingredient_name: number}
		self.ingredients_coordinates = []; # list of coordinates of every : [[x, y], ...]
		self.y = 8;
		self.x = 18;
		self.cooked = False;
		self.outgoings_expense = 0;

	#======================================================================
	
	def do_pizza(self):
		#Display of the pizza
		self.display_pizza_edge(4);

		curses.curs_set(2); # Show the cursor

		#Put ingredients on the pizza
		self.put_ingredients();

	#======================================================================

	def display_pizza(self, color_pair):
		self.scr.addstr(3,  14, ", - ~~ - ,", curses.color_pair(color_pair));
		self.scr.addstr(4,  10, ", '            ' ,", curses.color_pair(color_pair));
		self.scr.addstr(5,  8, ",                    ,", curses.color_pair(color_pair));
		self.scr.addstr(6,  7, ",                      ,", curses.color_pair(color_pair));
		self.scr.addstr(7,  6, ",                        ,", curses.color_pair(color_pair));
		self.scr.addstr(8,  6, ",                        ,", curses.color_pair(color_pair));
		self.scr.addstr(9,  6, ",                        ,", curses.color_pair(color_pair));
		self.scr.addstr(10, 7, ",                      ,", curses.color_pair(color_pair));
		self.scr.addstr(11, 8, ",                    ,", curses.color_pair(color_pair));
		self.scr.addstr(12, 10, ",                ,", curses.color_pair(color_pair));
		self.scr.addstr(13, 12, "' - , __ , - '", curses.color_pair(color_pair));
		self.scr.move(8, 18);
		self.scr.refresh();

	#======================================================================

	def display_pizza_edge(self, color_pair):
		self.scr.addstr(2,  5, "        , -  ~~  - ,        ", curses.color_pair(color_pair));
		self.scr.addstr(3,  5, "    , '              ' ,    ", curses.color_pair(color_pair));
		self.scr.addstr(4,  5, "  ,                      ,  ", curses.color_pair(color_pair));
		self.scr.addstr(5,  5, " ,                        , ", curses.color_pair(color_pair));
		self.scr.addstr(6,  5, ",                          ,", curses.color_pair(color_pair));
		self.scr.addstr(7,  5, ",                          ,", curses.color_pair(color_pair));
		self.scr.addstr(8,  5, ",                          ,", curses.color_pair(color_pair));
		self.scr.addstr(9,  5, ",                          ,", curses.color_pair(color_pair));
		self.scr.addstr(10, 5, ",                          ,", curses.color_pair(color_pair));
		self.scr.addstr(11, 5, " ,                        , ", curses.color_pair(color_pair));
		self.scr.addstr(12, 5, "  ,                      ,  ", curses.color_pair(color_pair));
		self.scr.addstr(13, 5, "    ,                  ,    ", curses.color_pair(color_pair));
		self.scr.addstr(14, 5, "      ' - ,  __  , - '      ", curses.color_pair(color_pair));
		self.scr.move(8, 18);
		self.scr.refresh();

	#======================================================================

	def correct_position(self):
		dx = abs(17 - self.x);
		dy = abs(8 - self.y)*2.5;
		d = math.sqrt(dx**2 + (dy**2));

		if(d < 11):		
			for i in self.ingredients_coordinates:
				if (i[0] == self.x and i[1] == self.y):
					return(False);

			return(True);

		else:
			return(False);
	
	#======================================================================

	def overdraft(self, ingredient):
		if(self.restaurant.debit(self.restaurant.ingredients[ingredient], self.constant_scr)):
			self.outgoings_expense += self.restaurant.ingredients[ingredient];
			return(False);

		else:
			return(True);

	#======================================================================

	def put_ingredients(self):
		key = self.scr.getkey().lower();

		while(key.lower() != 'q'):
			#Movements
			if(key == 'key_right'):
				self.x += 2 if self.x <= 37 else 0;

			elif(key == 'key_left'):
				self.x -= 2 if self.x >= 1 else 0;

			elif(key == 'key_up'):
				self.y -= 1 if self.y >= 1 else 0;

			elif(key == 'key_down'): 
				self.y += 1 if self.y <= 18 else 0; 

			# Check if player want to cook the pizza
			elif(key == 'e'):
				self.cook();

			elif(key == 't'):
				if(not self.overdraft(self.restaurant.connection_key_ingredient['t'])):
					self.display_pizza(1);
					try:
						self.ingredients_on_pizza["tomato"] += 1;
					except KeyError:
						self.ingredients_on_pizza["tomato"] = 1;

			#Put an ingredient
			elif(key in self.restaurant.connection_key_ingredient.keys()):
				self.add_ingredient(self.restaurant.connection_key_ingredient[key]);

			self.scr.move(self.y, self.x);
			key = self.scr.getkey().lower();
	
		self.client.served();

	#======================================================================

	def add_ingredient(self, which_one):
		if(self.correct_position() and not self.overdraft(which_one)):		
			self.scr.addstr(self.y, self.x, emoji.emojize(":"+which_one+":"));
			self.ingredients_coordinates.append([self.x, self.y]);

			try:
				self.ingredients_on_pizza[which_one] += 1;
			except KeyError:
				self.ingredients_on_pizza[which_one] = 1;

			self.scr.refresh();
	
	#======================================================================

	def cook(self):
		time.sleep(self.restaurant.cooking_time);
		self.cooked = True;
		self.display_pizza_edge(1);
		try:
			if (self.ingredients_on_pizza["tomato"] >= 1):
				self.display_pizza(1);
		except KeyError:
			pass;
