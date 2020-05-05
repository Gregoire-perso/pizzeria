# class of the thread that display client satisfaction for waiting time

# Global import
import time;
import curses;
from threading import Thread;

class WaitingTime(Thread):
	def __init__(self, restaurant, pizza, const_scr, main_scr):
		super().__init__();
		self.restaurant = restaurant;
		self.pizza = pizza;
		self.main_scr = main_scr;
		self.const_scr = const_scr;
		self.stop = False;
		self.waiting_rate = 100;
	
	def run(self):
		while (not self.stop):
			self.restaurant.display_waiting_rate(self.const_scr, self.waiting_rate);
			#self.main_scr.move(self.pizza.y, self.pizza.x);
			time.sleep(2);
			#curses.setsyx(1, 1);
			self.waiting_rate -= 1.0;
	
	def stop_thread(self):
		self.stop = True;

