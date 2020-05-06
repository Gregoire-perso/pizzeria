# Client file
"""
Client documentation

Properties:
>>> int nb_pizza : "number of wanted pizza"
>>> window scr : "main screen"
>>> window command_scr : "screen that display the command of the client for the current pizza"
>>> window keys_scr : "screen that display connections between keys and ingredients"
>>> window constant_scr : "screen that show money left, level, number of day, ..."
>>> Restaurant restaurant : "restaurant object (the player)"
>>> list ingredient_choice : "ingredients that are wanted on the pizza"
>>> int price : "price of the pizza (without margin)"
>>> Pizza current_pizza : "pizza that is cooked"
>>> int payement : "price decided by the client"
>>> int outgoings_expense : "outgoings expense for every pizza of the client"

Methods:
>>> __init__(self, Restaurant restaurant, window scr window command_scr, window keys_scr, window constant_scr) : "same as properties"
	construtor of the client
>>> generate_command(self)
	generation of th command
>>> display_command(self)
	display the command and the connection between keys and ingredients
>>> served(self)
	success rate the pizza and pay the player acording to the success rate
"""
# Global import
import random;
import time;
import json;
import math;

# Local import
import Pizza;

class Client:
	def __init__(self, restaurant, scr, command_scr, keys_scr, constant_scr):
		self.nb_pizzas = 1; # Possible improvment
		self.scr = scr;
		self.command_scr = command_scr;
		self.keys_scr = keys_scr;
		self.constant_scr = constant_scr;
		self.restaurant = restaurant;
		self.generate_command();
		self.outgoings_expense = 0;
		self.display_command();
		self.restaurant.display_budget(self.constant_scr);
		self.current_pizza = Pizza.Pizza(self, self.restaurant, self.ingredient_choice, self.scr, constant_scr); # Creation of the pizza object
		self.current_pizza.do_pizza();
	
	#===========================================================================================
	
	def generate_command(self):
		with open("../languages/french/orders.json", "r") as f:
			orders = json.load(f);

		order_choice = random.sample(orders.keys(), 1);
		
		ingredient_unavaible = False;
		for i in order_choice:
			if (i not in self.restaurant.ingredients):
				ingredient_unavaible = True;

		if (ingredient_unavaible):
			self.generate_command();
		else:
			self.ingredient_choice = "".join(order_choice).split(", ");

	#===========================================================================================

	def display_command(self):
		self.command_scr.clear();
		self.keys_scr.clear();
		with open("../languages/french/orders.json", "r") as f:
			command = json.load(f)[", ".join(self.ingredient_choice)];
			self.command_scr.addstr(0, 0, command);
		
		temp = list(self.restaurant.connection_key_ingredient_display.items());
		for i in range(len(self.restaurant.connection_key_ingredient) + 1):
			self.keys_scr.addstr(i, 0, temp[i][0] + " : " + temp[i][1]);

		self.command_scr.refresh();
		self.keys_scr.refresh();

	#===========================================================================================

	def served(self):
		self.wait.stop_thread();
		waiting_time = self.wait.waiting_rate;
		self.wait.join();
		ingredients_wanted_on_pizza = self.current_pizza.ingredients_on_pizza;
		unwanted_ingredients = 0;
		
		# Calculation of unwanted ingredients
		for elt, number in self.current_pizza.ingredients_on_pizza.items():
			if(not elt in self.ingredient_choice):
				unwanted_ingredients += number;
				del ingredients_wanted_on_pizza[elt];

		# If there are more than 8 ingredients of the same type, the other ingredients of that type are not taking into consideration
		temp = ingredients_wanted_on_pizza;
		for elt, number in temp.items():
			if (number > 8):
				ingredients_wanted_on_pizza[elt] = 8;

		# Calculation of the ingredients rate
		ingredients_success_rate = sum(ingredients_wanted_on_pizza.values()) / (len(self.ingredient_choice) * 8) * 100;
		ingredients_success_rate -= unwanted_ingredients * 2;

		# Calculation of cooking rate
		cooking_rate = 1 if self.current_pizza.cooked else 0.90

		# Calculation of waiting rate
		if (waiting_time >= 90):
			waiting_rate = 1.10;

		elif (waiting_time >= 80):
			waiting_rate = 1;
		
		elif (waiting_time >= 70):
			waiting_rate = 0.90;
		
		elif (waiting_time >= 60):
			waiting_rate = 0.80;
		
		elif (waiting_time >= 50):
			waiting_rate = 0.70;
		
		else:
			waiting_rate = 0.50;

		# Calculation of the global rate
		global_success_rate = ingredients_success_rate * cooking_rate * waiting_rate;

		with open("../packages/all_ingredients.json", "r") as f:
			prices = json.load(f);
			self.minimum_price = sum([prices[i] * ingredients_wanted_on_pizza[i] for i in ingredients_wanted_on_pizza.keys()]) + 2;
		
		self.payement = round(self.minimum_price * (1 * (global_success_rate/100)), 2);
		self.restaurant.credit(self.payement, self.constant_scr);
		self.outgoings_expense += self.current_pizza.outgoings_expense;
		self.restaurant.xp += self.payement;

