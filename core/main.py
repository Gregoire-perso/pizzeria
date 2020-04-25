# Global import
import curses;

# Local import
import master;
import Day;

def end_day():
	choice = master.end_day_menu(main_scr);

	if (choice == '1'):
		restaurant.upgrade_menu(main_scr);
		end_day();
	
	elif (choice == '2'):
		new_day();
	
	elif (choice == '3'):
		master.save_game(restaurant);
		end_day();
	
	elif (choice == '4'):
		return (0);
	


def new_day():
	day = Day.Day(restaurant, main_scr, command_scr, keys_scr, constant_scr);
	day.start_day();

	end_day();


def main(screen):
	"""Main function"""
	global restaurant, main_scr, command_scr, keys_scr, constant_scr;
	
	main_scr, command_scr, keys_scr, constant_scr = master.init(screen);

	if (master.start_menu(main_scr) == '1'):
		restaurant = master.load_game(main_scr);
	
	else:
		restaurant = master.new_game(main_scr);
	
	new_day();


curses.wrapper(main);

