from database import Database
from menu import Menu

# connect to MongoDB and switch to database
Database.initialize()

# instantiate a Menu instance
menu = Menu()

# launch the menu
menu.run_menu()
