#Minesweeper clone
#Version 1.0 
#6/15/16

import random
import tkinter as tk
buttons = []
time_elapsed = int(0)
class Board:
    """Class to hold a "minesweeper" board"""
    def __init__(self, height, width, mines, mine_x = None, mine_y = None):
        self.height = height
        self.width = width
        self.mines = mines
        self.flagged = 0
        self.cleared = 0
        self.board = []
        self.game_over = False

    #Places the mines on the board
    def place_mines(self):
        """Places the mines on the board"""
        placed = False
        mine_count = 0
        #Place each mine under a unique tile
        for i in range(self.mines):
            while not placed:
                x = random.randrange(self.width)
                y = random.randrange(self.height)
                if (self.board[x][y] == ' '):
                    self.board[x][y] = '*'
                    placed = True
                    mine_count += 1
                else:
                    placed = False
            placed = False
        return 0
    #Adds the numbers showing how many mines surround a tile
    def add_numbers(self):
        """Adds numbers indicating how many mines surround a tile"""
        count = 0
        for i in range(self.width):
            for j in range(self.height):
                if (self.board[i][j] != '*'):
                    count = self.surround_board(i, j, '*')
                if (count):
                    self.board[i][j] = str(count)
                    count = 0
        return 0
    
    #Write function to generate board
    def generate(self, mine_x, mine_y):
        #Create an empty board
        #The top left square is (0,0)
        self.board = []
        for i in range(self.width):
            i = []
            for j in range(self.height):
                i.append(' ')
            self.board.append(i)
        #If we were passed a cleared tile, clear it before placing mines
        if (mine_x and mine_y):
            self.board[mine_x][mine_y] = 'c'

        self.place_mines()

        #If we were passed a cleared tile, return it to a normal tile
        if (mine_x and mine_y):
            self.board[mine_x][mine_y] = ' '

        self.add_numbers()
        self.print()
        pass

    #The function called when you click on a mine
    def check(self, x, y, clear=False):
        """Main logic function. Runs a check on the clicked tile to deterine what to do"""
        #Prevents clearing a flagged square or clearing squares once the game is won
        print("Check function")
        if (buttons[x][y]["text"] == 'F' or self.game_over):
            #Do nothing
            return 0

        #If the first tile clicked is a mine, generate a new board and click on it
        if (self.board == []):
            #Generate a new board with that tile pre-cleared
            global board
            board.generate(x, y)
            #Call check on the new board
            board.check(x, y)
            timer.start()
            return 0
        
        #If we clicked on a square that was already cleared and was a number
        if ((buttons[x][y]["text"] >= '0' and buttons[x][y]["text"] <= '8') and clear):
            #If enough surrounding mines are cleared, treat this as an empty square and "click" on all surrounding tiles
            #Clicks on flagged tiles will be ignored, as always
            count = self.surround_buttons(x, y, 'F')
            if (count == int(buttons[x][y]["text"])):
                self.board[x][y] = ' '
                self.clear(x, y)
            return 0
        #If it was an empty square, do nothing
        elif (self.board[x][y] == 'c'):
            #Do nothing
            return 0
    
        #Reveal the tile to the user
        buttons[x][y]["text"] = self.board[x][y]
        #Make the button look disabled
        buttons[x][y]["relief"] = "sunken"
        buttons[x][y]["highlightcolor"] = "black"
        buttons[x][y]["fg"] = "white"
        #Set a flag to indicate that the tile was cleared
        buttons[x][y]["command"] = lambda x=x, y=y: board.check(x, y, True)
        
        #If the user clicked on a mine, BOOM
        if (self.board[x][y] == "*"):
            print("Game over")
            #Reveal all mines
            self.game_end()

        #If we have a completely empty tile, clear it and surrounding tiles
        elif (self.board[x][y] == ' '):
            #Completely empty tile
            buttons[x][y]["background"] = "black"
            self.cleared += 1
            #Clear surrounding spaces
            self.clear(x, y)

        #If we have a tile with mines around it, only clear this tile
        elif (self.board[x][y] >= '0' or self.board[x][y] <= '8'):
            #Tile with surrounding mines
            buttons[x][y]["background"] = "black"
            self.cleared += 1
            self.board[x][y] = 'c'

        #If all the tiles that aren't mines are cleared, the game is won
        if (self.width*self.height - self.mines == self.cleared):
            print("You Win")
            self.game_end(win=True)

    def game_end(self, win=False):
        """Reveal all mines and whether they were correctly flagged"""
        self.game_over = True
        timer.stop()
        for i in range(self.width):
            for j in range(self.height):
                buttons[i][j]["state"] = "disabled"
                if (self.board[i][j] == '*'):
                    #If a mine was flagged or the game was won, make the tile green
                    if (buttons[i][j]["text"] == 'F' or win):
                        buttons[i][j]["background"] = "green"
                    #If a mine was not flagged correctly, make the tile red
                    else:
                        buttons[i][j]["background"] = "red"
                        buttons[i][j]["text"] = "*"

    def print(self):
        """Prints the entire board to the terminal"""
        for i in self.board:
            print(i)

    #Clicks on flagged tiles will always be ignored
    def flag(self, event, x, y):
        """Flags or unflags the passed tile"""
        #If the button is disabled or a cleared space, 
        if not (buttons[x][y]["state"] == "disabled" or buttons[x][y]["relief"] == "sunken"):
            if (buttons[x][y]["text"] == ' '):
                buttons[x][y]["text"] = 'F'
                self.flagged += 1
            elif(buttons[x][y]["text"] == 'F'):
                buttons[x][y]["text"] = ' '
                self.flagged -= 1
            #Update the counter
            app.flagged["text"] = "Flagged: " + str(self.flagged) + "/" + str(self.mines)
        return 0

    #Runs the check function on each mine surrounding the given mine
    def clear(self, x, y):
        """Clears the tiles surrounding the passed tile"""
        #If a square has already been cleared, ignore it
        if (self.board[x][y] != 'c'):
            self.board[x][y] = 'c'
            if (x > 0):
                #We can check the tile on the left
                self.check(x-1, y)
                #We can check the tile above and on the left
                if (y < (self.height-1)):
                    self.check(x-1, y+1)
                #We can check the tile below and on the left
                if (y > 0):
                    self.check(x-1, y-1)
            #We can check the tile on the right
            if (x < (self.width-1)):
                self.check(x+1, y)
                #We can check the tile above and on the right
                if (y < (self.height-1)):
                    self.check(x+1, y+1)
                #We can check the tile below and on the right
                if (y > 0):
                    self.check(x+1, y-1) 
            #We can check the tile below
            if (y > 0):
                self.check(x, y-1)
            #We can check the tile above
            if (y < (self.height-1)):
                self.check(x, y+1)
    #Counts the number of items surrounding a square, such as mines
    def surround_board(self, x, y, char='c'):
        """Counts the mines surrounding a tile"""
        count = 0
        #We can check the tile on the left
        if (x > 0):
            if (self.board[x-1][y] == char):
                count += 1
            #We can check the tile above and on the left
            if (y < (self.height-1)): 
                if (self.board[x-1][y+1] == char):
                    count += 1
            #We can check the tile below and on the left
            if (y > 0): 
                if (self.board[x-1][y-1] == char):
                    count += 1 
        #We can check the tile on the right
        if (x < (self.width-1)): 
            if (self.board[x+1][y] == char):
                count += 1
            #We can check the tile above and on the right
            if (y < (self.height-1)):
                if (self.board[x+1][y+1] == char):
                    count += 1
            #We can check the tile below and on the right
            if (y > 0): 
                if (self.board[x+1][y-1] == char):
                    count += 1 
        #We can check the tile below
        if (y > 0):
            if (self.board[x][y-1] == char):
                count += 1
        #We can check the tile above
        if (y < (self.height-1)): 
            if (self.board[x][y+1] == char):
                count += 1
        return count
    #Count the items shown to the user surrounding a square (such as flags)
    def surround_buttons(self, x, y, char='F'):
        """Counts the flagged squares surrounding a tile"""
        count = 0
        #We can check the tile on the left
        if (x > 0):
            if (buttons[x-1][y]["text"] == char):
                count += 1
            #We can check the tile above and on the left
            if (y < (self.height-1)): 
                if (buttons[x-1][y+1]["text"] == char):
                    count += 1
            #We can check the tile below and on the left
            if (y > 0): 
                if (buttons[x-1][y-1]["text"] == char):
                    count += 1 
        #We can check the tile on the right
        if (x < (self.width-1)): 
            if (buttons[x+1][y]["text"] == char):
                count += 1
            #We can check the tile above and on the right
            if (y < (self.height-1)):
                if (buttons[x+1][y+1]["text"] == char):
                    count += 1
            #We can check the tile below and on the right
            if (y > 0): 
                if (buttons[x+1][y-1]["text"] == char):
                    count += 1 
        #We can check the tile below
        if (y > 0):
            if (buttons[x][y-1]["text"] == char):
                count += 1
        #We can check the tile above
        if (y < (self.height-1)): 
            if (buttons[x][y+1]["text"] == char):
                count += 1
        return count

class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.create_menu()
        self.master.title("Finesweeper")
        self.option_window = None

    def create_menu(self):
        """Creates the menu"""
        #Creates the frame to hold the menu
        menu_frame = tk.Frame()
        #Create and place the Custom Game button
        self.configure = tk.Button(master = menu_frame, text = "Custom Game", command = self.options_window)
        self.configure.grid(row = 1, column = 1)
        #Create and place the New Game button
        self.new_game = tk.Button(master = menu_frame, text = 'New Game', command = lambda: app.create_game(board.width, board.height, board.mines))
        self.new_game.grid(row = 1, column = 2)
        #Create and place the Flagged counter
        self.flagged = tk.Label(master = menu_frame, text = "Flagged: 0")
        self.flagged.grid(row = 1, column = 3)
        #Create and place the timer
        self.timer = tk.Label(master = menu_frame, text = 'Time: 0')
        self.timer.grid(row = 1, column = 4)
        #Place the menu_frame in the main grid
        menu_frame.grid(row = 1, column = 1, sticky = 'N')
        #Set a flag for proper resizing
        root.columnconfigure(1, weight = 1)

    def create_minefield(self):
        """Creates and sets up the grid of tiles"""
        #Create the frame to hold the minefield
        minefield = tk.Frame()
        #Generate the minefield
        for i in range(board.width):
            buttons2 = []
            for j in range(board.height):
                #Tie the left click to the check function
                buttons2.append(tk.Button(master = minefield, text = ' ', command = lambda x=i, y=j: board.check(x, y)))
                #Make each button resizable
                buttons2[j].grid(row=i, column=j, sticky="NSEW")
                #Tie the right-click to flag a mine
                buttons2[j].bind("<Button-3>", lambda event, x=i, y=j: board.flag(event, x, y))
                buttons2[j]["height"] = 2
                buttons2[j]["width"] = 2        
            buttons.append(buttons2)
        for i in range(board.width):
            minefield.columnconfigure(i, weight = 1)
        for j in range(board.height):
            minefield.rowconfigure(j, weight = 1)
        #Place the minefield frame in the main grid
        minefield.grid(row = 2, column = 1, sticky = "NESW")
        #Set the proper weight for resizing
        root.rowconfigure(2, weight = 1)

    def destroy_custom_window(self):
        self.option_window.destroy()
        self.option_window = None
        return 0

    def options_window(self):
        """Launches the custom game window"""
        #If the custom game window exists, don't open a new one
        if (self.option_window):
            print("Custom game window already open")
            return 0
        #Create new window
        self.option_window = tk.Toplevel(self)
        #Set the window title
        self.option_window.title("Custom Game")
        #Override the close button behavior
        self.option_window.protocol("WM_DELETE_WINDOW", self.destroy_custom_window)
        #Create the options list
        tk.Label(self.option_window, text = "Width").grid(row = 1, column = 1)
        width = tk.Entry(self.option_window, width = 5)
        width.grid(row = 1, column = 2)
        tk.Label(self.option_window, text = "Height").grid(row = 2, column = 1)
        height = tk.Entry(self.option_window, width = 5)
        height.grid(row = 2, column = 2)
        tk.Label(self.option_window, text = "Mines").grid(row = 3, column = 1)
        mines = tk.Entry(self.option_window, width = 5)
        mines.grid(row = 3, column = 2)
        #Create and place the create button
        create_button = tk.Button(self.option_window, text = "Create", command = lambda: self.create_game(int(width.get()), int(height.get()), int(mines.get()), destroy=True) )
        create_button.grid(row = 4, column = 1)
        #Create and place the close button
        close_button = tk.Button(self.option_window, text = "Close", command = self.destroy_custom_window)
        close_button.grid(row = 4, column = 2)

    def destroy_tiles(self):
        """Destroys all the tiles"""
        for x in range(board.width):
            for y in range(board.height):
                buttons[x][y].destroy()

    def error(self, message):
        self.error_window = tk.Toplevel(self)
        tk.Label(self.error_window, text = message).grid(row = 1, column = 1)
        tk.Button(self.error_window, text = "Ok", command = self.error_window.destroy).grid(row = 2, column = 1)
        self.error_window.grab_set()
        return 0

    def create_game(self, width, height, mines, destroy=False):
        """Creates a new game based on passed parameters"""
        #Check to make sure the game is valid
        if (height <= 0 or width <= 0 or mines < 0):
            self.error("Invalid board")
            return 0
        if (height*width <= mines):
            self.error("There are no free tiles with the selected options.")
            return 0
        #If we came from the custom game dialog, close it
        if destroy:
            self.destroy_custom_window()
            self.option_window = None
        global buttons
        #If we had a game, destroy each button
        if buttons:
            self.destroy_tiles()
            buttons = []
        #Generate a new board
        global board
        board = Board(height, width, mines)
        timer.reset()
        #Create a fresh instance of the GUI
        self.create_menu()
        self.flagged["text"] = ("Flagged: " + str(board.flagged) + "/" + str(board.mines))
        self.create_minefield()
        board.print()

class Timer():
    """Simple timer. Likely somewhat accurate"""
    def __init__(self):
        self.elapsed = 0
        self.run = 0
    def increment(self):
        if (self.run):
            self.elapsed += 1
            app.after(1000, self.increment)
        app.timer["text"] = "Time: " + str(self.elapsed)
    def reset(self):
        """Resets the timer to 0"""
        self.run = 0
        self.elapsed = 0
        app.timer["text"] = "Time: " + str(self.elapsed)
    def stop(self):
        """Stops the timer without losing the current elapsed time"""
        self.run = 0
    def start(self):
        """Starts the timer"""
        if not self.run:
            self.run = 1
            app.after(1000, self.increment) 


#Create a default board 
board = Board(16, 16, 40)
#Create an instance of the timer
timer = Timer()
#Start the GUI
root = tk.Tk()
app = GUI(master=root)
app.mainloop()