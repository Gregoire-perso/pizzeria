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

# Local import
import Restaurant;

def init(main_screen):
	"""Main function"""
	# Colors init #
	curses.init_color(8, 800, 600, 0);
	curses.init_color(9, 999, 800, 0);
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK);
	curses.init_pair(3, 8, curses.COLOR_BLACK);
	curses.init_pair(4, 9, curses.COLOR_BLACK);
	curses.curs_set(0);
	main_scr = curses.newwin(20, 70, 8, 0); # The main self.main_screen
	command_scr = curses.newwin(3, 60, 4, 0); # The command self.main_screen
	keys_scr = curses.newwin(20, 40, 8, 40); # self.main_screen that display connection between key and ingredient
	constant_scr = curses.newwin(3, 60, 0, 0); # self.main_screen that display money, day, etc...
	main_scr.keypad(True);

	return(main_scr, command_scr, keys_scr, constant_scr);

def start_menu(main_scr):
	"""Function that manage the start menu"""
	main_scr.clear();

	main_scr.addstr(3, 5, "Menu principal");
	main_scr.addstr(4, 5, "1 : Charger une partie");
	main_scr.addstr(5, 5, "2 : Nouvelle partie");
	
	key = '100';
	while(key not in '12'):
		key = main_scr.getkey();
	
	return(key);

#================================================================

def end_day_menu(main_scr):
	main_scr.clear();
	
	main_scr.addstr(3, 2, "Que voulez-vous faire ?");
	main_scr.addstr(4, 2, "1 : Améliorer votre restaurant (pas dispo)");
	main_scr.addstr(6, 2, "2 : Ouvrir la pizzeria le lendemain");
	main_scr.addstr(7, 2, "3 : Sauvegarder votre partie (rien ne se passe, c'est normal)");
	main_scr.addstr(9, 2, "4 : Quitter (sans sauvegarder)");

	key = '100';
	while(key not in '1234'):
		key = main_scr.getkey();
	
	main_scr.clear();

	return(key);

#=================================================================

def existing_game(game):
	"""str game --> bool
	Check is the game \'game\' already exist or not"""
	
	return(os.path.exists("../games/" + game));

#================================================================

def load_game(main_scr):
	"""Funciton that will load an existing game"""
	main_scr.clear();
	curses.curs_set(2); # Show the cursor
	curses.echo();
	main_scr.addstr(3, 5, "Quel est votre nom ? ");
	name = main_scr.getstr().decode("utf-8");

	while(not existing_game(name)):
		main_scr.clear();
		main_scr.addstr(3, 5, "Cette sauvegarde n'existe pas... (Veillez à respecter la casse)");
		main_scr.addstr(4, 5, "Entrez le nom d'une sauvegarde : ");
		name = main_scr.getstr().decode("utf-8");
		
	curses.noecho();
	curses.curs_set(0); # Hide the cursor

	with open("../games/" + name + "/restaurant.save", "rb") as restaurant_file: # Get the Player object
		restaurant_ = pickle.load(restaurant_file);
	
	return(restaurant_);

#================================================================

def save_game(restaurant):
	os.mkdir("../games/" + restaurant.name);
	with open("../games/" + restaurant.name + "/restaurant.save", "wb") as f:
		pickle.dump(restaurant, f);

#=================================================================

def new_game(main_scr):
	"""Function that create a new game"""
	curses.curs_set(2); # Show the cursor
	main_scr.clear(); # Clear the main_screen
	curses.echo(); # Display what the user is writting

	main_scr.addstr(3, 5, "Quel est votre prénom ? ");
	surname = main_scr.getstr().decode("utf-8");
	main_scr.addstr(4, 5, "Quel est votre nom ? ");
	name = main_scr.getstr().decode("utf-8");

	while(existing_game(name)): # Check if the game already exists
		main_scr.clear();
		main_scr.addstr(3, 5, "Cette partie existe déjà...")
		main_scr.addstr(4, 5, "Quel est votre prénom ? ");
		surname = main_scr.getstr().decode("utf-8");
		main_scr.addstr(5, 5, "Quel est votre nom ? ");
		name = main_scr.getstr().decode("utf-8");
		
	curses.noecho(); # Hide typed character
	curses.curs_set(0); # Hide the cursor

	restaurant_ = Restaurant.Restaurant(name, surname);

	return(restaurant_);

