# Day managment file

# Global import
import math;
import random;
import time;

# Local import
import Client;

class Day:
	def __init__(self, restaurant, main_scr, command_scr, keys_scr, const_scr):
		self.restaurant = restaurant;
		self.number_of_client = abs(random.randint(round(math.log10(restaurant.xp)**2) - 2, round(math.log10(restaurant.xp)**2) + 2)) + 1;
		self.main_scr = main_scr;
		self.keys_scr = keys_scr;
		self.command_scr = command_scr;
		self.const_scr = const_scr;
		self.income_of_the_day = 0;
		self.outgoings_expense_of_the_day = 0;
		self.start_day();

	def start_day(self):
		for i in range(self.number_of_client):
			current_client = Client.Client(self.restaurant, self.main_scr, self.command_scr, self.keys_scr, self.const_scr);
			current_client.current_pizza.do_pizza();
			self.income_of_the_day += current_client.payement;
			self.outgoings_expense_of_the_day += current_client.outgoings_expense;
			self.main_scr.clear();
			self.command_scr.clear();
			self.keys_scr.clear();
			self.main_scr.refresh();
			self.keys_scr.refresh();
			self.command_scr.refresh();
			time.sleep(random.randint(0, 2));
		
		self.end_of_day()
	
	def end_of_day(self):
		self.restaurant.debit(10, self.const_scr); # Payement of the rent
		self.main_scr.clear();
		self.keys_scr.clear();
		self.command_scr.clear();
		
		self.main_scr.addstr(2, 2, "Dépense du jour");
		self.main_scr.addstr(3, 2, "  Ingrédients : {0}€".format(self.outgoings_expense_of_the_day));
		self.main_scr.addstr(4, 2, "  Loyer : {0}€".format(self.restaurant.rent));
		
		self.main_scr.addstr(5, 2, "Entrées du jour");
		self.main_scr.addstr(6, 2, "  Payement des pizzas : {0}€".format(self.income_of_the_day));

		self.main_scr.addstr(7, 2, "Nombre de clients aujourd'hui : {0}".format(self.number_of_client));

		self.main_scr.refresh();
		self.keys_scr.refresh();
		self.command_scr.refresh();

		self.main_scr.getkey();
