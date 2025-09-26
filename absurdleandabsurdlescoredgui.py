"""
to help with structure:
https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
"""

import tkinter as tk
import absurdlescoredcl
import absurdlev2
import enchant
import random
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage 
import PIL
from PIL import Image 
from random import sample
import string

# constants: number of word sin wordlist dependning on difficulty mode
BEG_MODE_NO = 100
INT_MODE_NO = 300
ADV_MODE_NO = 500

# constants: for scoring / score penalties 
INITIAL_SCORE = 100
HINT_PENALTY = 5
GUESS_PENALTY = 10
SEE_ORIGINAL_WORDLIST_PENALTY = 5
SEE_CURRENT_WORDLIST_PENALTY = 30


DICT = enchant.Dict("en_GB") #for validating user input 

WORDLIST_FILE = "wordlists/absurdleguigamewords.txt" # from https://gist.github.com/shmookey/b28e342e1b1756c4700f42f17102c2ff

class AbsurdleGameGui(tk.Tk):
    
    
    def __init__(self, root):
        #initializing window
        root.title("Absurdle Games")
        root.geometry('1000x1000')
        root.resizable(False,False)
        root['bg'] = "white"

        #initializing variables - belong to instance of class 
        self.original_wordlist = ["this", "has", "not", "updated"]
        self.current_wordlist = ["this", "also", "has", "not", "updated", "yet"]
        self.score = INITIAL_SCORE
        self.guess_feedback_current_row = 0
        self.current_guess = ""
        self.totalWords = 0
        self.instructions = ""

        # images used for widgets - belong to instance of class 
        self.logo = PhotoImage(file= "images/logo.png").subsample(2,2)
        self.alogo = PhotoImage(file= "images/alogo.png").subsample(2,2)
        self.aoras = PhotoImage(file = "images/absurdleorabsurdle-scored.png").subsample(3, 3)
        self.welcomeabsurdle = PhotoImage(file = "images/welcomeabsurdle.png").subsample(3, 3)
        self.welcomescored = PhotoImage(file = "images/welcomeabsurdlescored.png").subsample(3, 3)
        self.startimage = PhotoImage(file= "images/start.png").subsample(5, 5)
        self.askInstructions = PhotoImage(file= "images/askInstructions.png").subsample(3, 3)
        self.aslogo = PhotoImage(file= "images/aslogo.png").subsample(2,2)
        self.yesplease = PhotoImage(file= "images/yesplease.png").subsample(7, 7)
        self.nothanks = PhotoImage(file= "images/nothanks.png").subsample(7, 7)
        self.alogosmall = PhotoImage(file= "images/alogo.png").subsample(5,5)
        self.aslogosmall = PhotoImage(file= "images/aslogo.png").subsample(5, 5)
        self.finishedreading = PhotoImage(file= "images/finishedreading.png").subsample(6, 6)
        self.selectdifflevel = PhotoImage(file= "images/selectdifflevel.png").subsample(3, 3)
        self.beginner = PhotoImage(file= "images/beginner.png").subsample(7, 7)
        self.intermediate = PhotoImage(file= "images/intermediate.png").subsample(7, 7)
        self.advanced = PhotoImage(file= "images/advanced.png").subsample(7, 7)
        self.enterguess = PhotoImage(file= "images/enterguess.png").subsample(17, 17)
        self.submit = PhotoImage(file= "images/submit.png").subsample(25, 25)
        self.returntohome = PhotoImage(file= "images/returntohome.png").subsample(9, 9)
        self.randomguess= PhotoImage(file= "images/randomguess.png").subsample(15, 15)
        self.wordlistfullscreentext = PhotoImage(file= "images/wordlistfullscreentext.png").subsample(2, 2)
        self.continuelabel = PhotoImage(file= "images/continuelabel.png").subsample(12, 12)
        self.scorelabel = PhotoImage(file= "images/score.png").subsample(10, 10)
        self.originalwordlistlabel = PhotoImage(file= "images/originalwordlistlabel.png").subsample(9, 9)
        self.possiblesecretwordslabel = PhotoImage(file= "images/possiblesecretwords.png").subsample(9, 9)
        self.getahintlabel = PhotoImage(file= "images/getahintlabel.png").subsample(9, 9)
        self.instructionslabel = PhotoImage(file= "images/instructionslabel.png").subsample(9, 9)

        self.AInstructions = PhotoImage(file= "images/Ainstructions.png").subsample(2, 2)
        self.page1ASInstructions = PhotoImage(file= "images/page1ASinstructions.png").subsample(2, 2)
        self.page2ASInstructions = PhotoImage(file= "images/page2ASInstructions.png").subsample(2, 2)
        self.nextpage = PhotoImage(file= "images/next.png").subsample(8, 8)

        self.gameover = PhotoImage(file = "images/gameoverbetter.png").subsample(2, 2)
        self.playagain = PhotoImage(file = "images/playagain.png").subsample(5, 5)
        self.yeslabel = PhotoImage(file = "images/yes.png").subsample(20, 20)
        self.nolabel = PhotoImage(file = "images/no.png").subsample(20, 20)
        self.gamewonlabel = PhotoImage(file = "images/gamewon.png").subsample(5,5)
        self.gamewonguessesimage = PhotoImage(file = "images/gamewonguesses.png").subsample(5, 5)



        
        

        #WIDGETS- belomg to instance of class 
        #for welcome page
        self.logo_label = tk.Label(root, image=self.logo, bd = 0) #https://www.geeksforgeeks.org/how-to-add-an-image-in-tkinter/
        self.welcome_label = tk.Label(root, image = self.aoras, bd = 0)
        self.choose_absurdle_button = tk.Button(root, image = self.alogosmall, command=self.absurdle_start)
        self.choose_absurdle_scored_button = tk.Button(root, image = self.aslogosmall, command=self.absurdle_scored_start)
        
        #for absurdle start pages 
        self.alogo_label = tk.Label(root, image=self.alogo, bd = 0) 
        self.absurdle_welcome_label = tk.Label(root, image = self.welcomeabsurdle, bd = 0)
        self.absurdle_start_button = tk.Button(root, image = self.startimage, command=self.absurdle_ask_instructions)
        self.absurdle_ask_instructions_label = tk.Label(root, image = self.askInstructions, bd = 0)
        self.absurdle_yes_instructions_button = tk.Button(root, image = self.yesplease, command=self.show_instructions, bd = 0)
        self.absurdle_no_instructions_button = tk.Button(root, image = self.nothanks, command = self.absurdle_no_instructions, bd = 0)

        #for instructions 
        self.AInstructions_label = tk.Label(root, image=self.AInstructions, bd = 0)
        self.page1ASInstructions_label = tk.Label(root, image=self.page1ASInstructions, bd = 0)
        self.page2ASInstructions_label = tk.Label(root, image=self.page2ASInstructions, bd = 0)
        self.next_page_button = tk.Button(root, image = self.nextpage, command = self.next_page)
        self.absurdle_finished_reading_button = tk.Button(root, image = self.finishedreading, command = self.absurdle_clear_instructions)

        #for absurdle-scored start pages 
        self.aslogo_label = tk.Label(root, image=self.aslogo, bd = 0) 
        self.absurdle_scored_welcome_label = tk.Label(root,image = self.welcomescored, bd = 0)
        self.absurdle_scored_start_button = tk.Button(root, image = self.startimage, command=self.absurdle_scored_ask_instructions)
        self.absurdle_scored_ask_instructions_label = tk.Label(root, image = self.askInstructions, bd = 0)
        self.absurdle_scored_yes_instructions_button = tk.Button(root, image = self.yesplease, command=self.show_instructions)
        self.absurdle_scored_no_instructions_button = tk.Button(root, image = self.nothanks, command = self.absurdle_scored_no_instructions)
        self.absurdle_scored_instructions_label = tk.Label(root, text = "ABSURDLE-SCORED GAME INSTRUCTIONS: PROVISIONAL INSTRUCTONS")
        self.absurdle_scored_finished_reading_button = tk.Button(root, image = self.finishedreading, command = self.absurdle_scored_clear_instructions)
        self.pick_mode_label = tk.Label(root, image = self.selectdifflevel, bd = 0)
        self.beginner_button = tk.Button(root, image = self.beginner, command = self.set_mode_to_beginner) 
        self.intermediate_button = tk.Button(root, image = self.intermediate, command = self.set_mode_to_intermediate)
        self.advanced_button = tk.Button(root, image = self.advanced, command = self.set_mode_to_advanced)

        
        #for displaying wordlist in absurdle-scored
        self.wordlist_label = tk.Label(root, text = f"This is the wordlist for the current game. Click continue when you feel ready. Seeing the original wordlist after this point will result in a penalty of {SEE_ORIGINAL_WORDLIST_PENALTY}.", pady = 10)
        self.wordlist_label = tk.Label(root, image = self.wordlistfullscreentext, bd = 0)
        self.wordlist_text_fullscreen = tk.Text(root, width = 1000, height = 32, wrap='word', padx = 10, bd = 0, font=('Arial', 11, 'bold'))
        self.wordlist_continue_button = tk.Button(root, image = self.continuelabel, command = self.continue_from_wordlist)

        self.letter_buttons = {}
        for uppercase_letter in string.ascii_uppercase:
                button = tk.Button(root, text=uppercase_letter, width=1, height=1, command=lambda letter=uppercase_letter: self.enter_letter(letter), bg="white")
                self.letter_buttons[uppercase_letter] = button

        #backspace button
        self.backspace_button = tk.Button(root, text="Backspace", width=10, height=1, command= self.backspace, bg="white")

        #to allow user to submit guess 
        self.guess_label = tk.Label(root, image=self.enterguess, bd = 0)
        self.guess_entry = tk.Entry(root, text= "guess")
        self.guess_entry.bind("<Return>", self.submit_guess_enter) #https://www.geeksforgeeks.org/how-to-bind-the-enter-key-to-a-tkinter-window/ - to allow guess to be submitted by pressing enter button on keyboard
        self.guess_submit_button = tk.Button(root, image = self.submit, command =self.submit_guess)
        self.incorrect_guess_label = tk.Label(root, text = f"Enter a valid word", fg= "red") #for incorrect  guesses 

        #buttons for absurdle scored game page - to see wordlist, possible secret words, and hints, to see instructions, and return to home page 
        self.display_wordlist_option_button = tk.Button(root, image = self.originalwordlistlabel, command = lambda : self.open_wordlist_popup(root, "original"))
        self.display_pruned_wordlist_option_button = tk.Button(root, image = self.possiblesecretwordslabel, command = lambda : self.open_wordlist_popup(root, "current"))
        self.display_hints_option_button = tk.Button(root, image = self.getahintlabel, command = lambda : self.open_hints_popup(root, self.current_wordlist))
        self.display_instructions_option_button = tk.Button(root, image = self.instructionslabel, command = lambda : self.open_instructions_popup(root))
        self.return_to_home_button = tk.Button(root, image = self.returntohome, command = self.return_to_home)

        #to display score 
        self.score_label2 = tk.Label(root, image = self.scorelabel, bd = 0)
        self.score_label = tk.Label(root, text = self.score) 
        
        #button for submitting random guesses 
        self.random_guess_button = tk.Button(root, image = self.randomguess, command = self.submit_random_guess, bg = "white")

        #feedback frame - grey rectangle with feedback for words submitted 
        self.feedback_frame = tk.Frame(root, width = 300, height = 600)
        self.feedback_canvas = tk.Canvas(root) # use a canvas to allow scrollability
     
        
       
        #for making feedback frame scollable using https://blog.teclado.com/tkinter-scrollable-frames/#:~:text=In%20Tkinter%2C%20only%20the%20Canvas,That's%20what%20scrolling%20really%20is!
        self.scrollbar = ttk.Scrollbar(self.feedback_frame, orient="vertical", command=self.feedback_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.feedback_canvas)
        
        #for case of game over 
        self.gameover_label = tk.Label(root, image = self.gameover)
        self.ask_restart_label = tk.Label(root, image = self.playagain, bd = 0)
        self.restart_yes_button = tk.Button(root, image = self.yeslabel, command = self.restart)
        self.restart_no_button = tk.Button(root, image = self.nolabel, command = self.exitprog)

        #for case of game won 
        self.gamewon_label = tk.Label(root, image = self.gamewonlabel, bd = 0)
        self.gamewonguesses_label = tk.Label(root, image = self.gamewonguessesimage, bd = 0)
        self.finalscore = tk.Label(root, text = self.score, font = ('Arial', 20, 'bold'), bg = "white")
        self.number_of_guesses = 0
        self.finalnumberofguesses = tk.Label(root, text = self.number_of_guesses, font = ('Arial', 20, 'bold'), bg = "white")

        self.game_version = "" # will be A if absurdle or AS if absurdle-scored 


    """
    for displaying start page widgets- choosing absurdle or absurdle-scored 
    """
    def start(self):
        self.logo_label.pack()
        self.welcome_label.pack()
        self.choose_absurdle_button.pack()
        self.choose_absurdle_scored_button.pack()

    """
    for clearing widgets from start page
    """
    def clear_welcome(self):
        self.logo_label.pack_forget()
        self.welcome_label.pack_forget()
        self.choose_absurdle_button.pack_forget()
        self.choose_absurdle_scored_button.pack_forget()
    
    """
    for displaying widgets for welcome to absurdle 
    """
    def absurdle_start(self):
        self.game_version = "A"
        self.clear_welcome()
        self.alogo_label.pack()
        self.absurdle_welcome_label.pack()
        self.absurdle_start_button.pack()
        self.original_wordlist = self.absurdle_get_wordlist()
        self.current_wordlist = self.original_wordlist

    """
    for displaying welcome to absurdle-scored widgets
    """
    def absurdle_scored_start(self):
        self.game_version = "AS"
        self.clear_welcome()
        self.aslogo_label.pack()
        self.absurdle_scored_welcome_label.pack()
        self.absurdle_scored_start_button.pack()

    """
    for displaying widgets asking for instructions for absurdle 
    """
    def absurdle_ask_instructions(self):
        self.absurdle_start_button.pack_forget()
        self.absurdle_welcome_label.pack_forget()
        self.absurdle_ask_instructions_label.pack()
        self.absurdle_yes_instructions_button.pack()
        self.absurdle_no_instructions_button.pack()
    
    """
    for displaying widgets asking for instructions for absurdle-scored 
    """
    def absurdle_scored_ask_instructions(self):
        self.absurdle_scored_start_button.pack_forget()
        self.absurdle_scored_welcome_label.pack_forget()
        self.absurdle_scored_ask_instructions_label.pack()
        self.absurdle_scored_yes_instructions_button.pack()
        self.absurdle_scored_no_instructions_button.pack()
    
    """ for showing instructions for either absurdle or absurdle-scored"""
    def show_instructions(self):
        self.alogo_label.pack_forget()
        self.aslogo_label.pack_forget()
        if self.game_version == "AS": # if current game is absurdle-scored 
            self.absurdle_scored_ask_instructions_label.pack_forget()
            self.absurdle_scored_yes_instructions_button.pack_forget()
            self.absurdle_scored_no_instructions_button.pack_forget()
            self.page1ASInstructions_label.pack()
            self.next_page_button.pack()
        else: # if current game is absurdle 
            self.absurdle_ask_instructions_label.pack_forget()
            self.absurdle_yes_instructions_button.pack_forget()
            self.absurdle_no_instructions_button.pack_forget()
            self.AInstructions_label.pack()
            self.absurdle_finished_reading_button.pack()
        
    """
    for displaying second page of instructions for absurdle-scored 
    """
    def next_page(self):
        self.page1ASInstructions_label.pack_forget()
        self.next_page_button.pack_forget()
        self.page2ASInstructions_label.pack()
        self.absurdle_scored_finished_reading_button.pack()  
    
    """
    for clearing widgets asking user if they want instructions (absurdle)
    """
    def absurdle_clear_instruction_options(self):
        self.absurdle_ask_instructions_label.pack_forget()
        self.absurdle_yes_instructions_button.pack_forget()
        self.absurdle_no_instructions_button.pack_forget()
        self.alogo_label.pack_forget()

    """
    for clearing widgets asking user if they want instructions (absurdle-scored)
    """
    def absurdle_scored_clear_instruction_options(self):
        self.absurdle_scored_ask_instructions_label.pack_forget()
        self.absurdle_scored_yes_instructions_button.pack_forget()
        self.absurdle_scored_no_instructions_button.pack_forget()
        self.aslogo_label.pack_forget()
    
    """
    for clearing instructions for absurdle and getting widgets for absurdle game play 
    """
    def absurdle_clear_instructions(self):
        self.AInstructions_label.pack_forget()
        self.absurdle_finished_reading_button.pack_forget()
        self.get_absurdle_widgets() # for displaying widgets for absurdle gameplay
        self.ask_for_guess()

    """
    for clearing instructions for absurdle-scored and giving options of difficulty mode
    """
    def absurdle_scored_clear_instructions(self):
        self.page2ASInstructions_label.pack_forget()
        self.absurdle_scored_finished_reading_button.pack_forget()
        self.give_mode_options() # to give difficulty mode options 
    
    """
    for getting absurdle game play widgets if user does not want instructions
    """
    def absurdle_no_instructions(self):
        self.absurdle_clear_instruction_options()
        self.get_absurdle_widgets()
        self.ask_for_guess()

    """
    for going straight to giving mode options if no instructions wanted for absurdle-scored 
    """
    def absurdle_scored_no_instructions(self):
        self.absurdle_scored_clear_instruction_options()
        self.give_mode_options()

    """
    for getting instructions for absurdle 
    """
    def absurdle_get_wordlist(self):
        with open("wordlists/absurdleguigamewords.txt", 'r') as file: # wordlist is always the same 
            self.all_words_in_file = file.readlines() # reads all words from file 
        formatted_lines = []
        for line in self.all_words_in_file: #to create formatted list 
            formatted_lines.append(line.strip().upper())
        return formatted_lines

    """
    for getting instructions for absurdle-scored 
    """
    def absurdle_scored_get_wordlist(self):
        with open(WORDLIST_FILE, 'r') as file:
            self.all_words_in_file = file.readlines()
        subset_lines = sample(self.all_words_in_file, self.totalWords) # chooses random words from all_words_in_files - the number of words depends on the difficulty mode chosen
        formatted_lines = []
        for line in subset_lines: #to create formatted list
            formatted_lines.append(line.strip().upper()) 
        return formatted_lines
      
        
    """
    to get wordlist when beginner mode selected in absurdle-scored 
    """
    def set_mode_to_beginner(self):
        self.clear_mode_options() # clears difficulty mode options 
        self.totalWords = BEG_MODE_NO
        self.original_wordlist = self.absurdle_scored_get_wordlist()
        self.current_wordlist = self.original_wordlist
        self.display_wordlist_fullscreen()

    """
    to get wordlist when intermediate mode selected in absurdle-scored 
    """
    def set_mode_to_intermediate(self):
        self.clear_mode_options() # clears difficulty mode options 
        self.totalWords = INT_MODE_NO
        self.original_wordlist = self.absurdle_scored_get_wordlist()
        self.current_wordlist = self.original_wordlist
        self.display_wordlist_fullscreen()

    """
    to get wordlist when advanced mode selected in absurdle-scored 
    """
    def set_mode_to_advanced(self):
        self.clear_mode_options()
        self.totalWords = ADV_MODE_NO
        self.original_wordlist = self.absurdle_scored_get_wordlist()
        self.current_wordlist = self.original_wordlist
        self.display_wordlist_fullscreen()
    
    """
    to get widgets for absurdle game play widgets 
    """
    def get_absurdle_widgets(self):
        self.display_instructions_option_button.place(x=770, y=15)
        self.return_to_home_button.place(x=770, y=200)
        self.get_keyboard() # for onscreen keyboard
        self.display_feedback_frame() # for feedback about guesses for user 
        self.random_guess_button.place(x = 450, y = 900)
    
    """
    to get widgets for absurdle scored game play
    """
    def get_absurdle_scored_widgets(self):
        self.display_wordlist_option_button.place(x=755, y=15)
        self.display_pruned_wordlist_option_button.place(x=755, y=200)
        self.display_hints_option_button.place(x=755, y=385)
        self.display_instructions_option_button.place(x = 755, y = 570)
        self.return_to_home_button.place(x=755, y=755)
        self.score_label2.place(x = 20, y =15)
        self.score_label.place(x = 240, y = 32)
        self.score_label.config(text= self.score,  font=('Arial', 25), bg = "white")
        self.get_keyboard()
        self.display_feedback_frame()
        self.random_guess_button.place(x = 450, y = 900)

    """
    to get widgets to give difficulty mode options for absurdle_scored
    """
    def give_mode_options(self):
        self.pick_mode_label.pack()
        self.beginner_button.pack()
        self.intermediate_button.pack()
        self.advanced_button.pack()

    """
    for clearing widgets for picking difficulty mode 
    """
    def clear_mode_options(self):
        self.pick_mode_label.pack_forget()
        self.beginner_button.pack_forget()
        self.intermediate_button.pack_forget()
        self.advanced_button.pack_forget()
        #self.ask_for_guess()
        
    """
    for absurdle-scored to display wordlist which takes up whole page 
    """
    def display_wordlist_fullscreen(self):
        self.wordlist_label.pack()
        self.wordlist_text_fullscreen.pack()
        self.wordlist_text_fullscreen.config(state = NORMAL) # to allow text to be editable
        self.wordlist_text_fullscreen.delete(1.0, tk.END) #to delete all words in textbox - for when game is played multiple times 
        self.wordlist_text_fullscreen.insert(tk.END, ", ".join(self.original_wordlist)) #to inset original_wordlist words into textbox 
        self.wordlist_text_fullscreen.config(state = DISABLED) # so textbox no longer editable
        self.wordlist_continue_button.pack()
    
    """
    to clear widgets for wordlist display and display absurdle-scored widgets needed for gameplay 
    """
    def continue_from_wordlist(self):
        self.wordlist_label.pack_forget()
        self.wordlist_text_fullscreen.pack_forget()
        self.wordlist_continue_button.pack_forget()
        self.get_absurdle_scored_widgets()
        self.ask_for_guess() # widgets allowing user to make a guess 
        
    """
    widgets for allowing user to make a guess 
    """
    def ask_for_guess(self):
        self.guess_label.pack()
        self.guess_entry.pack()
        self.guess_submit_button.pack()

    """
    for calculating how much entering a guess will prune the wordlist to give hint to user 
    """
    def calculate_hint_result(self, top_hints, hint_entry):
        hintWord = hint_entry.get().upper()
        if self.check_word(hintWord):
            self.incorrect_hint_label.pack_forget()
            buckets = absurdlev2.generateBuckets(hintWord, self.current_wordlist)
            wordlistAfterHint = absurdlev2.getBiggestBucketWords(buckets, absurdlev2.getBiggestBucketPattern(buckets)) # calculates this by counting words in biggest bucket after choosing this word 
            self.display_hint_result(top_hints, hintWord, wordlistAfterHint)
        else:
            self.incorrect_hint_label.pack()
    

    """
    For giving user feedback after they enter a hint word. Also updates the score. 
    """
    def display_hint_result(self, top_hints, hintWord, wordlistAfterHint):
        self.hint_result_label = tk.Label(top_hints, text = f"Choosing the word {hintWord} will reduce the number of possible solution words to {str(len(wordlistAfterHint))}") #number of words in biggest bucket
        self.hint_result_label.pack()
        self.score = self.score - HINT_PENALTY # will deduct 5 points off score for each hint word 
        self.score_label.config(text= self.score) # updates score label 
        self.check_game_over("no pattern") #checks game over now that score has been changed 

    """
    For displaying the wordlist in the popup window 
    """
    def open_wordlist_popup(self, root, type):
        if type == "current": #if user wants to see pruned, updated word list 
            wordlist = self.current_wordlist
            self.score = self.score - SEE_CURRENT_WORDLIST_PENALTY # -30 points 
        else: # if user wants to see the original word list 
            wordlist = self. original_wordlist
            self.score = self.score - SEE_ORIGINAL_WORDLIST_PENALTY # -5 points
        self.score_label.config(text= self.score) # updates score label 
        #https://www.tutorialspoint.com/how-do-i-create-a-popup-window-in-tkinter#:~:text=Popup%20window%20in%20Tkinter%20can,windows%20defined%20in%20any%20application.
        top_wordlist = Toplevel(root) # to create popup window 
        top_wordlist.geometry("750x250")
        top_wordlist.title("Words")
        self.wordlist_text = tk.Text(top_wordlist, width = 250, height = 250, font=('Arial', 11, 'bold'))
        self.wordlist_text.delete(1.0, tk.END) # to clear previous text 
        self.wordlist_text.insert(tk.END, "\n".join(wordlist)) # to insert word list into textbox 
        self.wordlist_text.config(state = DISABLED) #so cannot edit text 
        self.wordlist_text.pack(side=tk.LEFT)
        self.check_game_over("no pattern") #as score has changed, need to check not out of points 
        top_wordlist.after(10000, top_wordlist.destroy) # wordlist is only temporarily displayed to make it harder for user 
    
    """
    To open popup window displaying wordlist 
    """
    def open_instructions_popup(self, root):
        top_instructions = Toplevel(root) # to create popup window 
        top_instructions.geometry("900x800")
        top_instructions.title("Instructions")
        text_file = ""
        if self.game_version == "AS": # instructions depend on game version 
           text_file = "instructions/absurdleScoredInstructions.txt"
        else:
            text_file = "instructions/absurdleInstructions.txt"
        with open(text_file, 'r') as file: # reads instructions from correct text file 
            self.instructions = file.read()
        self.instructions_popup_text = tk.Text(top_instructions, width = 250, height = 250, wrap='word', padx = 10, pady = 10, font=('Arial', 11, 'bold'))
        self.instructions_popup_text.delete(1.0, tk.END) # delete what was previously in textbox from previous game 
        self.instructions_popup_text.insert(tk.END, self.instructions) # update textbox with instructions 
        self.instructions_popup_text.config(state = DISABLED) # text box uneditable
        self.instructions_popup_text.pack(side=tk.LEFT)

    """
    For displaying popup window for giving hints about words 
    """
    def open_hints_popup(self, root, wordlist):
        top_hints = Toplevel(root)
        top_hints.geometry("900x500")
        top_hints.title("Hints Window")

        self.hint_label = tk.Label(top_hints, text = f"Enter words you would like to know the outcome for (penalty = {absurdlescoredcl.HINT_PENALTY})")
        self.hint_entry = tk.Entry(top_hints, text= "word") # entry box for submitting a hint 
    
        self.hint_entry.delete(0, END)
        self.submit_button = tk.Button(top_hints, text = "Submit", command = lambda: self.calculate_hint_result(top_hints, self.hint_entry)) # button for submitting hint
        self.incorrect_hint_label = tk.Label(top_hints, text = f"Enter a valid word", fg= "red") # for if user submits an invalid hint word 
        self.hint_label.pack()
        self.hint_entry.pack()
        self.submit_button.pack()
    
    """
    buttons for onscreen keyboard - buttons start off white 
    """
    def get_keyboard(self):
        """tinkering around 31/03"""
        self.letter_buttons["Q"].place(x=325, y=800)
        self.letter_buttons["W"].place(x=360, y=800)
        self.letter_buttons["E"].place(x=395, y=800)
        self.letter_buttons["R"].place(x=430, y=800)
        self.letter_buttons["T"].place(x=465, y=800)
        self.letter_buttons["Y"].place(x=500, y=800)
        self.letter_buttons["U"].place(x=535, y=800)
        self.letter_buttons["I"].place(x=570, y=800)
        self.letter_buttons["O"].place(x=605, y=800)
        self.letter_buttons["P"].place(x=640, y=800)
        self.letter_buttons["A"].place(x=345, y=830)
        self.letter_buttons["S"].place(x=380, y=830)
        self.letter_buttons["D"].place(x=415, y=830)
        self.letter_buttons["F"].place(x=450, y=830)
        self.letter_buttons["G"].place(x=485, y=830)
        self.letter_buttons["H"].place(x=520, y=830)
        self.letter_buttons["J"].place(x=555, y=830)
        self.letter_buttons["K"].place(x=590, y=830)
        self.letter_buttons["L"].place(x=625, y=830)
        self.letter_buttons["Z"].place(x=365, y=860)
        self.letter_buttons["X"].place(x=400, y=860)
        self.letter_buttons["C"].place(x=435, y=860)
        self.letter_buttons["V"].place(x=470, y=860)
        self.letter_buttons["B"].place(x=505, y=860)
        self.letter_buttons["N"].place(x=540, y=860)
        self.letter_buttons["M"].place(x=575, y=860)
        for button in self.letter_buttons.values():
            button.config(bg = "white")
        self.backspace_button.place(x=620, y=860) # backspace button 

    "for entering letters into guess entry box"
    def enter_letter(self, letter):
        self.guess_entry.insert(END,letter)
    
    """
    to delete letters for guess entry box using backspace button 
    """
    def backspace(self):
        entry = self.guess_entry.get()
        if entry:
            self.guess_entry.delete(len(entry) -1, END) # deletes last character from entry box 
            
    """
    For displaying grey rectangle with feedback for words submitted so far 
    """
    def display_feedback_frame(self):
        #the following lines adapted code from https://blog.teclado.com/tkinter-scrollable-frames/
        self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.feedback_canvas.configure(
        scrollregion=self.feedback_canvas.bbox("all"))) # to allow the feedback frame to be scrollable 
        self.feedback_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.feedback_canvas.configure(yscrollcommand=self.scrollbar.set) 
        self.scrollbar.config(command=self.feedback_canvas.yview)
        self.feedback_frame.place(x= 320, y=130, width = 400, height = 650)
        self.feedback_canvas.place(x= 320, y=130, width = 350, height = 650)
        self.scrollbar.pack(side="right", fill="y")

        self.feedback_canvas.yview_moveto(0.0) #so that view is at the top of the feedback frame 

    """
    for sumbitting a guess 
    """
    def submit_guess(self):
        guess_str = self.guess_entry.get().upper()
        if (self.check_word(guess_str) == True):
            self.incorrect_guess_label.pack_forget() # if up from a previous invalid guess 
            if (self.game_version == "AS"):
                self.score = self.score - GUESS_PENALTY #takes penalty if playoing absurdle-scored 
                self.score_label.config(text= self.score) # updates score labvel 
            if (self.game_version == "A"):
                self.number_of_guesses = self.number_of_guesses + 1 # counts number of guesses for absurdle for final feedback on game 
            current_pattern = self.update_feedback_frame(guess_str) # updated feedback given in grey rectangle 
            self.guess_entry.delete(0, END)
            if (self.game_version == "AS"):
                self.check_game_over(current_pattern) # checks score not bellow or equal to 0 now 
        else: 
            self.guess_entry.delete(0, END) # if incorrect guess then deletes what was entered in entry box 
            self.incorrect_guess_label.pack() # and shows invalid message 
    
    """
    To allow user to submit guess using physical keyboard enter button 
    """
    def submit_guess_enter(self, event):
        self.submit_guess()
    
    """
    To allow user to submit a random gues using button 
    """
    def submit_random_guess(self):
        random_guess = random.choice(self.original_wordlist).upper() # random word from original wordlist 
        self.incorrect_guess_label.pack_forget()
        if (self.game_version == "AS"):
            self.score = self.score - GUESS_PENALTY # if in absurdle scored there is a penalty for making a guess 
            self.score_label.config(text= self.score) # updates score label 
        if (self.game_version == "A"):
                self.number_of_guesses = self.number_of_guesses + 1 # updates count of number of guesses made so far 
        current_pattern = self.update_feedback_frame(random_guess) # updates feedback frame with feedback from random guess 
        if ((self.game_version == "AS")):
                self.check_game_over(current_pattern) # as score has changed, checks that score is still above 0 

    """
    Guesses and hints must be 5 letters long and from imported dictionary 
    """
    def check_word(self, word):
        if not (len(word) == 5) or (not (DICT.check(word)) and not(word in self.original_wordlist)): 
            return False
        else:
            return True
        
    """
    To update feedback frame after a guess has been made 
    """
    def update_feedback_frame(self, guess_str):
        buckets = absurdlev2.generateBuckets(guess_str, self.current_wordlist)
        current_pattern = absurdlev2.getBiggestBucketPattern(buckets)
        self.create_labels_for_feedback_row(self.feedback_frame, guess_str, current_pattern) # for displaying word with correct patterned tiles 
        if (current_pattern == '🟩'* 5): # if all green tiles then must be game must be won 
            self.game_won()
        else:
            self.guess_feedback_current_row = self.guess_feedback_current_row + 1 # increments index for next guess 
            self.current_wordlist = absurdlev2.getBiggestBucketWords(buckets, current_pattern) # updates the wordlist based on guess made 
        return current_pattern

    """
    Gives a score to tile colour as green is more valuble feedback than yellow and yellow more valuble than grey and onscreen keyboard always gives most valuble information 
    """
    def colour_to_number(self, colour):
        colour_number = 0
        if colour == "green":
            colour_number = 3
        elif colour == "yellow":
            colour_number = 2
        elif colour == "darkgrey":
            colour_number = 1
        return colour_number
    """
    To alow user to scroll on feedback frame 
    """
    def scroll(self):
        bbox = self.feedback_canvas.bbox("all")
        if bbox and bbox[3] > self.feedback_canvas.winfo_height():
            self.feedback_canvas.yview_moveto(1.0)

#TODO can porbably shorten this code using a dictionary
    
    """
    to show feedback for a guess using coloured tiles 
    """
    def create_labels_for_feedback_row(self, feedback_frame, word, pattern):
        row_frame = tk.Frame(self.scrollable_frame)
        for i in range (5):
            letter = word[i]
            if pattern[i] == '🟩':
                letter_label = tk.Label(row_frame, text = word[i], width = 5, height = 2, bg = "green")
                new_colour = "green"
            elif pattern[i] == '🟨':
                letter_label = tk.Label(row_frame, text = word[i], width = 5, height = 2, bg = "yellow")
                new_colour = "yellow"
            else:
                letter_label = tk.Label(row_frame, text = word[i], width = 5, height = 2, bg = "darkgrey")
                new_colour = "darkgrey"
            letter_label.pack(padx=10, side = tk.LEFT)
            
            current_colour = self.letter_buttons[letter].cget("bg")
            if self.colour_to_number(current_colour) < self.colour_to_number(new_colour):
                    self.letter_buttons[letter].config(bg = f"{new_colour}")
        self.scrollable_frame.pack()
        row_frame.pack(pady=10)
        
        #the following lines adapted code from https://blog.teclado.com/tkinter-scrollable-frames/
        self.scrollable_frame.bind("<Configure>", lambda e: self.feedback_canvas.configure(scrollregion = self.feedback_canvas.bbox("all")))

        self.scrollable_frame.update_idletasks()
        self.feedback_canvas.configure(scrollregion=self.feedback_canvas.bbox("all"))
        self.feedback_canvas.itemconfig(self.feedback_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw"), width=self.scrollable_frame.winfo_reqwidth(), height=self.scrollable_frame.winfo_reqheight())
        
        if (self.guess_feedback_current_row > 10):
            #self.scrollable_frame.after(10, self.feedback_canvas.yview_moveto, 1.0) #https://stackoverflow.com/questions/76565478/making-scrollbar-to-scroll-towards-bottom-when-a-message-is-sent-using-customtki
            self.scrollable_frame.after(10, self.feedback_canvas.yview_scroll, 1, "units") #so that starts scrolling when too many guesses in feedback frame - will scroll to most recent guess 

    """
    To check if the game is over for absurdle-scored - score must be 0 or less and last gues mustn't have been the final secret word 
    """
    def check_game_over(self, current_pattern):
        if (self.score <= 0) and (current_pattern != '🟩'* 5):
            # clear all widgets for game play 
            packed_widgets = [self.guess_submit_button, self.guess_entry, self.guess_label, self.incorrect_guess_label]
            for widget in packed_widgets:
                widget.pack_forget()

            for child in self.scrollable_frame.winfo_children():
                child.destroy()

            widgets = [
            self.score_label, self.score_label2, self.display_hints_option_button, self.display_wordlist_option_button, self.display_pruned_wordlist_option_button, self.return_to_home_button, self.display_instructions_option_button,
            self.incorrect_guess_label, self.feedback_frame, self.feedback_canvas, self.random_guess_button,
            self.backspace_button]
            for button in self.letter_buttons.values():
                widgets.append(button)
            for widget in widgets:
                widget.place_forget()
            
            #widgets displayed for asking user if they want to play again 
            self.gameover_label.pack()
            self.ask_restart_label.pack()
            self.restart_yes_button.pack()
            self.restart_no_button.pack()

    """
    for clearing widgets for game play and displaying widgets associated with winning game 
    """       
    def game_won(self):
        #for clearing widgets for game play 
        packed_widgets = [self.guess_submit_button, self.guess_entry, self.guess_label, self.incorrect_guess_label]
        for widget in packed_widgets:
            widget.pack_forget()
        widgets = [
        self.score_label, self.score_label2, self.display_hints_option_button, self.display_wordlist_option_button,self.display_pruned_wordlist_option_button, self.return_to_home_button,self.display_instructions_option_button,
        self.incorrect_guess_label, self.random_guess_button, self.backspace_button #self.feedback_frame, self.feedback_canvas, 
        ]
        for button in self.letter_buttons.values():
            widgets.append(button)
        for widget in widgets:
            widget.place_forget()

        #label for absurdle scored tells user about their final score 
        if (self.game_version == "AS"):
            self.gamewon_label.pack()
            self.finalscore.place(x = 700, y = 50)
            self.finalscore.config(text = self.score)
        else: # label for absurdle scored tells user about number of guesses made 
            self.gamewonguesses_label.pack()
            self.finalnumberofguesses.place(x = 700, y = 50)
            self.finalnumberofguesses.config(text = self.number_of_guesses)

       #to display widgets asking user if they want to play again  
        self.ask_restart_label.place(x = 300, y = 800)
        self.restart_yes_button.place(x = 700, y = 850)
        self.restart_no_button.place(x = 700, y = 900)
        
    """
    For if user wants to play a game again 
    """
    def restart(self):
        self.original_wordlist = ["this", "has", "not", "updated"]
        self.current_wordlist = ["this", "also", "has", "not", "updated", "yet"]
        self.score = INITIAL_SCORE #score set back to 0 
        self.number_of_guesses = 0 # no guesses made yet 
        self.guess_feedback_current_row = 0 
        self.current_guess = ""
        self.totalWords = 0
        for child in self.scrollable_frame.winfo_children():
            child.destroy() # destroy what was in feedback frame from last game 

        #clearing widgets 
        self.feedback_frame.place_forget()
        self.feedback_canvas.place_forget()

        self.gamewon_label.pack_forget()
        self.gamewonguesses_label.pack_forget()
        self.finalscore.place_forget()
        self.finalnumberofguesses.place_forget()
        self.ask_restart_label.place_forget()
        self.restart_yes_button.place_forget()
        self.restart_no_button.place_forget()

        self.gameover_label.pack_forget()
        
        self.ask_restart_label.pack_forget()
        self.restart_yes_button.pack_forget()
        self.restart_no_button.pack_forget()

        self.start()    

    """
    To allow user to exit game 
    """          
    def exitprog(self):
        exit()

    """
    To allow user to return to home page 
    """
    def return_to_home(self):
        #clearing widgets 
        packed_widgets = [self.guess_submit_button, self.guess_entry, self.guess_label, self.incorrect_guess_label]
        for widget in packed_widgets:
            widget.pack_forget()

        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        widgets = [
        self.score_label, self.score_label2, self.display_hints_option_button, self.display_wordlist_option_button, self.display_pruned_wordlist_option_button, self.return_to_home_button,self.display_instructions_option_button,
        self.incorrect_guess_label, self.feedback_frame, self.feedback_canvas,self.random_guess_button, self.backspace_button]
        for button in self.letter_buttons.values():
            widgets.append(button)

        for widget in widgets:
            widget.place_forget()
        self.restart()

        

def main(): 
    root = Tk()
    absurdleGameGui = AbsurdleGameGui(root)
    absurdleGameGui.start()
    root.mainloop()

if __name__ == '__main__':
    main()



        
