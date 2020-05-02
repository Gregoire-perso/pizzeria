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
		self.price = 10; # Modifier le prix et tout le système de notation
		self.outgoings_expense = 0;
		self.display_command();
		self.current_pizza = Pizza.Pizza(self, self.restaurant, self.ingredient_choice, self.scr, constant_scr); # Creation of the pizza object
		self.payement = 0;
	
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
		unwanted_ingredients = 0;
		ingredient_success_rate = {} # Rating of the ingredient following the readme.md rules
		for elt, number in self.current_pizza.ingredients_on_pizza.items():
			if(not elt in self.ingredient_choice): # Check if there is a none wanted ingredient on the pizza
				unwanted_ingredients += number;

			else: # Check conditions of a good pizza on wanted ingredients
				ingredient_success_rate[elt] = number / 8 if number < 8 else 1;

		try:	
			global_ingredient_success_rate = sum(ingredient_success_rate.values()) / len(ingredient_success_rate); # Ingredients success_rate without unwanted ingredients
		except ZeroDivisionError:
			global_ingredient_success_rate = 0; # If there is no ingredients which are wanted

		global_ingredient_success_rate *= 1 - (unwanted_ingredients / 100); # Rating with unwanted ingredients
	
		if(self.current_pizza.cooked):
			global_pizza_success_rate = global_ingredient_success_rate * 100;

		else:
			global_pizza_success_rate = global_ingredient_success_rate * 0.75 * 100;

		self.restaurant.credit(self.price * (1 + 0.01 * global_pizza_success_rate), self.constant_scr);
		self.payement += self.price * (1 + 0.01 * global_pizza_success_rate);
		self.outgoings_expense += self.current_pizza.outgoings_expense;
		self.restaurant.xp += self.payement;

