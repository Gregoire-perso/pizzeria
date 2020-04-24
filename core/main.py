# Main file of the pizzeria
"""
Colors numbers:
0: BLACK
1: RED
2: GREEN
3: YELLOW
4: BLUE
5: MAGENTA
6: CYAN
7: WHITE
8: LIGHT YELLOW
9: DARK YELLOW
10: ???

Colors pairs:
0: WHITE / BLACK
1: RED / BLACK
2: YELLOW / BLACK
3: LIGHT YELLOW / BLACK
4: DARK YELLOW / BLACK
"""
# Global import
import curses;
import os;
import pickle;
import math;

# Local import
import Client;
import Restaurant;
import Day;

def start_menu(scr):
	"""Function that manage the start menu"""
	scr.clear();

	scr.addstr(3, 5, "Menu principal");
	scr.addstr(4, 5, "1 : Charger une partie");
	scr.addstr(5, 5, "2 : Nouvelle partie");
	
	key = '100';
	while(key not in '12'):
		key = scr.getkey();
	
	return(key);

#================================================================

def end_day_menu(scr):
	scr.clear();
	
	scr.addstr(3, 2, "Que voulez-vous faire ?");
	scr.addstr(4, 2, "1 : Améliorer votre restaurant (pas dispo)");
	scr.addstr(6, 2, "2 : Ouvrir la pizzeria le lendemain");
	scr.addstr(7, 2, "3 : Sauvegarder votre partie (rien ne se passe, c'est normal)");
	scr.addstr(9, 2, "4 : Quitter (sans sauvegarder)");

	key = '100';
	while(key not in '1234'):
		key = scr.getkey();
	
	scr.clear();

	return(key);

#=================================================================

def existing_game(game):
	"""str game --> bool
	Check is the game \'game\' already exist or not"""
	
	return(os.path.exists("../games/" + game));

#================================================================

def load_game(scr):
	"""Funciton that will load an existing game"""
	scr.clear();
	curses.curs_set(2); # Show the cursor
	curses.echo();
	scr.addstr(3, 5, "Quel est votre nom ? ");
	name = scr.getstr().decode("utf-8");

	while(not existing_game(name)):
		scr.clear();
		scr.addstr(3, 5, "Cette sauvegarde n'existe pas... (Veillez à respecter la casse)");
		scr.addstr(4, 5, "Entrez le nom d'une sauvegarde : ");
		name = scr.getstr().decode("utf-8");
		
	curses.noecho();
	curses.curs_set(0); # Hide the cursor

	with open("../games/" + name + "/restaurant.save", "rb") as restaurant_file: # Get the Player object
		restaurant_ = pickle.load(restaurant_file);
	
	return(restaurant_); # Return the restaurant object

#================================================================

def save_game(restaurant):
	with open("../games/" + restaurant.name + "/restaurant.save", "wb") as f:
		pickle.dump(restaurant, f);

#=================================================================

def new_game(scr):
	"""Funtion that create a new game"""
	curses.curs_set(2); # Show the cursor
	scr.clear(); # Clear the screen
	curses.echo(); # Display what the user is writting

	scr.addstr(3, 5, "Quel est votre prénom ? ");
	surname = scr.getstr().decode("utf-8");
	scr.addstr(4, 5, "Quel est votre nom ? ");
	name = scr.getstr().decode("utf-8");

	while(existing_game(name)): # Check if the game already exists
		scr.clear();
		scr.addstr(3, 5, "Cette partie existe déjà...")
		scr.addstr(4, 5, "Quel est votre prénom ? ");
		surname = scr.getstr().decode("utf-8");
		scr.addstr(5, 5, "Quel est votre nom ? ");
		name = scr.getstr().decode("utf-8");
		
	os.mkdir("../games/" + name);
	curses.noecho(); # Hide typed character
	curses.curs_set(0); # Hide the cursor

	restaurant_ = Restaurant.Restaurant(name, surname);

	return(restaurant_);
	
#=================================================================

def main(screen):
	"""Main function"""
	global test
	# Colors init #
	curses.init_color(8, 800, 600, 0);
	curses.init_color(9, 999, 800, 0);
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK);
	curses.init_pair(3, 8, curses.COLOR_BLACK);
	curses.init_pair(4, 9, curses.COLOR_BLACK);
	curses.curs_set(0);
	main_scr = curses.newwin(20, 40, 8, 0); # The main screen
	command_scr = curses.newwin(3, 60, 4, 0); # The command screen
	keys_scr = curses.newwin(20, 40, 8, 40); # Screen that display connection between key and ingredient
	constant_scr = curses.newwin(3, 60, 0, 0); # Screen that display money, day, etc...
	main_scr.keypad(True);
	
	menu_state = "start_menu";
	while(menu_state == "start_menu"): # Display the starting menu while don't have a player
		choice = start_menu(main_scr);
		if choice == '1':
			tmp = load_game(main_scr);

		else:
			tmp = new_game(main_scr);

		if(tmp != "start_game"):
			menu_state = "no_start_menu";
			restaurant = tmp;

	day = Day.Day(restaurant, main_scr, command_scr, keys_scr, constant_scr);


	menu_state = "end_day_menu"
	while (menu_state == "end_day_menu"):
		choice = end_day_menu(main_scr);
		
		if (choice == '1'): # Player want to upgrade his restaurant
			pass; # Do it later

		elif (choice == '2'):
			day = Day.Day(restaurant, main_scr, command_scr, keys_scr, constant_scr);

		elif (choice == '3'): # Player want to save his game
			save_game(restaurant);

		else:
			menu_state = "no_end_day_menu";

	test = restaurant.xp


curses.wrapper(main);
print(test)

