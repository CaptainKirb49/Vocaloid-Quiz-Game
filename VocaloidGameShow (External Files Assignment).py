###########################################################
#External Files Assignment - Vocaloid Game Show
#Aiden Mark
#March 30, 2023
###########################################################

#Credits
#https://www.pysimplegui.org/en/latest/
#https://www.w3schools.com/python/module_random.asp

#Importing Packages
import PySimpleGUI as sg
import pandas as pd
from audioplayer import AudioPlayer as ap
import datetime as dt
import random

#Setting theme
sg.theme("DarkBlue14")

#Variables
pref_dict = {}
score_dict = {}
score_data = []
awards_data = {}
delete_score = False
player1 = ''
awards_list = {'5streak': False, '10streak': False, '25streak': False, '0': False, 'LongRound': False, 'ShortRound': False, 'Legend': False}
game_type = ['image', 'singer', 'sample1', 'sample2', 'sample3', 'producer', 'japanese']
display_image = ''
jp_text = ''
song_text = ''
options = []
songs_list = []
answer = ''
round = 0
round_limit = 0
player_score = 0
streak = 0
iteration = 0
score_text = ''
top3_text = ''
award_title = ''
awards_text = ''
message = ''
reaction = ''
first_round = False

#Fail Safe Function
def default_files(type):
    global delete_score
    global awards_data
    if type == "p":
        #Preferences
        pref_dict['Japanese'] = False
        pref_dict['Challenge'] = False
        pref_dict['Volume'] = 100.0
    
        with open("PlayerPreferences.txt", 'w') as prefs:
            prefs.write(str(pref_dict))
            prefs.close()
    
    elif type == 's':
        #Scoreboard
        time_stamp = str(dt.datetime.now())
        score_dict[0] = "No_Player, 0"
        delete_score = True
        
        with open("Scoreboard.txt", 'w') as score:
            score.write(str(score_dict))
            score.close()
            
    elif type == 'a':
        #Achievements
        for i in awards_list:
            awards_data[i] = False
            
        with open("Achievements.txt", 'w') as awards:
            awards.write(str(awards_data))
            awards.close()
            
#Function for making a list of songs based off the csv data
def write_songs():
    temp_list = []
    for i in game_data['Name']:
        temp_list.append(i)
    return temp_list

#Opens and writes data from files to variables to be used later
#Also checks if file exists and calls the fail safe if it doesn't
try:
    with open("PlayerPreferences.txt", 'r') as prefs:
        pref_dict = eval(prefs.read())
        prefs.close()

except:
    with open("PlayerPreferences.txt", 'w') as prefs:
        default_files('p')
        prefs.close()
    
try:
    with open("Scoreboard.txt", 'r') as score:
        score_dict = eval(score.read())
        if score_dict == {0: "No_Player, 0"}:
            delete_score = True
        score.close()
        delete_score = False

except:
    with open("Scoreboard.txt", 'w') as score:
        default_files('s')
        delete_score = True
        score.close()

try:
    with open("Achievements.txt", 'r') as awards:
        awards_data = eval(awards.read())
        awards.close()
        
except:
    with open("Achievements.txt", 'w') as awards:
        default_files('a')

try:
    game_data = pd.read_csv("vocaloid_data.csv")
    
except:
    print("The vocaloid_data.csv file is missing! Download from, https://docs.google.com/spreadsheets/d/1sg6z-Ixtalpy9ATyyEjjnqT2L-91g22pV_6xrKKFANw/edit?usp=sharing and put into the game folder")
    
songs_list = write_songs()
    
#Layout function, makes windows to avoid tag conflicts
def make_window(type):
    global options
    #Main Menu Layout
    if type == "mm":
        main_menu = [ [sg.Push(), sg.Text("Welcome to the Vocaloid Quiz Game!", font=('times_new_roman', 24, 'bold')), sg.Push()],
                      [sg.Push(), sg.Image("images/TitleImage.png", pad=(20)), sg.Push()],
                      [sg.Push(), sg.Button("Play", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Scoreboard", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Achievements", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Options", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Exit", expand_x=True), sg.Push()] ]
        
        return sg.Window("Main Menu", main_menu)
    
    #Options Menu Layout
    elif type == 'op':
        options = [ [sg.Push(), sg.Text("Options", font=('times_new_roman', 18, 'bold'), pad=10), sg.Push()],
                    [sg.Push(), sg.Checkbox("Challenge Questions", font=('times_new_roman', 12), pad=20, default=pref_dict['Challenge']), sg.Push()],
                    [sg.Push(), sg.Slider(range=(0, 100), default_value=pref_dict['Volume'], orientation='h'), sg.Push()],
                    [sg.Push(), sg.Text("Slider Changes The Volume",font=('times_new_roman', 12)), sg.Push()],
                    [sg.Push(), sg.Button("Clear Save Data", pad=30, expand_x=True), sg.Push()],
                    [sg.Push(), sg.Button("Apply"), sg.pin(sg.Button("Exit", expand_x=True)), sg.Push()] ]
        
        return sg.Window("Options", options)
    
    #Player Name Menu Layout
    elif type == 'pn':
        player_name = [ [sg.Push(), sg.Text("What is your name?", font=('times_new_roman', 12), pad=20), sg.Push()],
                        [sg.Push(), sg.Input(pad=20), sg.Push()],
                        [sg.Push(), sg.Button("Enter", size=20), sg.pin(sg.Button("Exit", size=20)), sg.Push()] ]
        
        return sg.Window("Player Name", player_name)
    
    #Round Picker Menu Layout
    elif type == 'r':
        play_setup = [ [sg.Push(), sg.Slider(range=(1, 50), default_value=10, orientation='h'), sg.Push()],
                       [sg.Push(), sg.Text("Number of Rounds",font=('times_new_roman', 12)), sg.Push()],
                       [sg.Push(), sg.Button("Enter", size=20), sg.pin(sg.Button("Exit", size=20)), sg.Push()] ]
        
        return sg.Window("Round Picker", play_setup)
    
    #Image Question Layout
    elif type == 'im':
        image_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text("What is this song?", font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Image(source='images/' + display_image, pad=20), sg.Push()],
                           [sg.Push(), sg.Button(options[0], size=40), sg.pin(sg.Button(options[1], size=40)), sg.Push()],
                           [sg.Push(), sg.Button(options[2], size=40), sg.pin(sg.Button(options[3], size=40)), sg.Push()] ]
        
        return sg.Window("Game", image_question)
    
    #Scoreboard Menu Layout
    elif type == 's':
        scoreboard = [ [sg.Push(), sg.Text("Scoreboard", font=('times_new_roman', 18, 'bold'), pad=10), sg.Push()],
                       [sg.Push(), sg.Text("Top 3 Scores", font=('times_new_roman', 16, 'bold'), pad=10), sg.Push()],
                       [sg.Push(), sg.Text(top3_text, font=('times_new_roman', 12), pad=10), sg.Push()],
                       [sg.Push(), sg.Text("Last 10 Scores", font=('times_new_roman', 16, 'bold'), pad=10), sg.Push()],
                       [sg.Push(), sg.Text(score_text, font=('times_new_roman', 12), pad=10), sg.Push()] ]
        
        return sg.Window("Scoreboard", scoreboard)
    
    #Japanese title question
    elif type == 'tq':
        title_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text("What is this song?", font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text(jp_text, font=('times_new_roman', 18), pad=20), sg.Push()],
                           [sg.Push(), sg.Button(options[0], size=40), sg.pin(sg.Button(options[1], size=40)), sg.Push()],
                           [sg.Push(), sg.Button(options[2], size=40), sg.pin(sg.Button(options[3], size=40)), sg.Push()] ]
        
        return sg.Window("Game", title_question)
    
    #Singer Question
    elif type == 'sq':
        singer_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                            [sg.Push(), sg.Text("Who Sings " + song_text + "?", font=('times_new_roman', 12), pad=20), sg.Push()],
                            [sg.Push(), sg.Button(options[0], size=40), sg.pin(sg.Button(options[1], size=40)), sg.Push()],
                            [sg.Push(), sg.Button(options[2], size=40), sg.pin(sg.Button(options[3], size=40)), sg.Push()] ]
        
        return sg.Window("Game", singer_question)
    
    #Producer Question
    elif type == 'pq':
        producer_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                              [sg.Push(), sg.Text("Who Produced " + song_text + "?", font=('times_new_roman', 12), pad=20), sg.Push()],
                              [sg.Push(), sg.Button(options[0], size=40), sg.pin(sg.Button(options[1], size=40)), sg.Push()],
                              [sg.Push(), sg.Button(options[2], size=40), sg.pin(sg.Button(options[3], size=40)), sg.Push()] ]
        
        return sg.Window("Game", producer_question)
    
    #Sound Question
    elif type == 'sound_q':
        sound_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text("What is this song?", font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Button("Play", pad=20), sg.pin(sg.Button("Stop", pad=20)), sg.Push()],
                           [sg.Push(), sg.Button(options[0], size=40), sg.pin(sg.Button(options[1], size=40)), sg.Push()],
                           [sg.Push(), sg.Button(options[2], size=40), sg.pin(sg.Button(options[3], size=40)), sg.Push()] ]
        
        return sg.Window("Game", sound_question)
    
    #Awards Notification Menu
    elif type == 'aw':
        award_granted = [ [sg.Push(), sg.Text("YOU GOT AN ACHIEVEMENT!", font=('times_new_roman', 18, 'bold'), pad=10), sg.Push()],
                          [sg.Push(), sg.Text(award_title, font=('times_new_roman', 16, 'bold'), pad=10), sg.Push()],
                          [sg.Push(), sg.Image(source="miku/streak.png", pad=20), sg.Push()],
                          [sg.Push(), sg.Button("OK", size=20, pad=20), sg.Push()] ]

        return sg.Window("Award", award_granted)
    
    #Awards Menu Layout
    elif type == 'am':
        award_menu = [ [sg.Push(), sg.Text("Achievement Menu", font=('times_new_roman', 18, 'bold'), pad=10), sg.Push()],
                          [sg.Push(), sg.Text(awards_text, font=('times_new_roman', 16, 'bold'), pad=10), sg.Push()],
                          [sg.Push(), sg.Image(source="miku/" + reaction, pad=20), sg.Push()],
                          [sg.Push(), sg.Button("Exit", size=20, pad=20), sg.pin(sg.Button("Next", size=20, pad=20)), sg.Push()] ]

        return sg.Window("Awards", award_menu)
    
    #Message Layout
    elif type == 'miku':
        miku_message = [  [sg.Push(), sg.Text(message, font=('times_new_roman', 16, 'bold'), pad=10), sg.Push()],
                          [sg.Push(), sg.Image(source="miku/" + reaction, pad=20), sg.Push()],
                          [sg.Push(), sg.Button("OK", size=20, pad=20), sg.Push()] ]

        return sg.Window("Message", miku_message)
    
#Displays message    
def miku_message(m, r):
    global message
    global reaction
    
    message = m
    reaction = r + '.png'
    
    window = make_window('miku')
    
    window.read()
    
    window.close()
        
#Main Menu Function
def Main_Menu():    
    window = make_window('mm')
    
    event, values = window.read()
    
    if event == "Play":
        window.close()
        set_solo()
        
    elif event == "Scoreboard":
        window.close()
        scoreboard()
        
    elif event == "Achievements":
        window.close()
        award_menu()
        
    elif event == "Options":
        window.close()
        Options_Menu()
        
    else:
        window.close()
        miku_message("Bye Bye, see you next time!", 'bye')
        
#Award Menu
def award_menu():
    global awards_text
    global iteration
    global reaction
    
    #Sets variables to be used
    num_aw = 0
    aw_array = ["5 Streak", "10 Streak", "25 Streak", "0", "Long Round", "Short Round", "Long Round", "LEGEND"]
    awards = {}
    
    #Cycles through the array and determines if award has been collected, displays if it has
    for i in awards_data:
        if awards_data[i] == True:
            awards[i] = aw_array[num_aw]
            num_aw += 1
        else:
            awards[i] = "?????"
            num_aw += 1
            
    #Iteration for page # that the menu is on
    if iteration == 0:
        awards_text = awards['5streak']
        
    elif iteration == 1:
        awards_text = awards['10streak']
        
    elif iteration == 2:
        awards_text = awards['25streak']

    elif iteration == 3:
        awards_text = awards['0']

    elif iteration == 4:
        awards_text = awards['LongRound']

    elif iteration == 5:
        awards_text = awards['ShortRound']

    elif iteration == 6:
        awards_text = awards['Legend']
        
    if awards_text == "?????":
        reaction = 'err.png'
    else:
        reaction = 'streak.png'
    
    window = make_window('am')
    
    #Closes the window and resets the page count
    if iteration == 7:
        window.close()
        iteration = 0
    
    event, values = window.read()
    
    #Checks for which button was pressed, executes task for each scenario
    if event == "Next":
        window.close()
        iteration += 1
        award_menu()
    elif event == None or event == "Exit":
        iteration = 0
        window.close()
        Main_Menu()

#Scoreboard Menu Function
def scoreboard():
    global score_text
    global top3_text
    score_text = ''
    score_data = []
    limit = 10
    top3_scores = []
    top3_text = ''
    
    #10 last scores
    if not score_dict == {0: "No_Player, 0"}:
        for i in score_dict.keys():
            score_data.append(i)
        score_data.reverse()
        
        for i in range(len(score_data)):
            if i < limit:    
                key = score_data[i]
                score_text = score_text + score_dict[key]['name'] + ", " + str(score_dict[key]['score']) + "pts : " + score_dict[key]['date'] + "\n\n"
        
        #Top 3 scores
        for i in score_data:
            if len(score_data) < 3: 
                top3_text = "There's not enough scores to show this portion, go play some more"
            else:
                top3_scores.append([i, score_dict[i]['score']]) 
                top3_scores.sort(reverse=True, key=sort)
                
        #Displaying the top 3 scores
        if len(score_data) < 3:
                top3_text = "There's not enough scores to show this portion, go play some more"
        else:
            for i in range(0, 3):
                top3_text = top3_text + score_dict[top3_scores[i][0]]['name'] + ", " + str(score_dict[top3_scores[i][0]]['score']) + "pts : " + score_dict[top3_scores[i][0]]['date'] + "\n\n"
        
        window = make_window('s')
        
        event, values = window.read()
        
        window.close()
        Main_Menu()
            
    else:
        Main_Menu()
        
#Sorting function
def sort(e):
    return e[1]

#Options Menu Function
def Options_Menu():
    window = make_window('op')
    event, values = window.read()
    
    if event == "Apply":
        window.close()
        apply_prefs(values)
    elif event == "Exit":
        Main_Menu()
        window.close()
    elif event == 'Clear Save Data':
        window.close()
        clear_save()
    else:
        Main_Menu()
        window.close()

#Clearing all saved data from external files
def clear_save():
    global awards_data
    global pref_dict
    global score_dict
    global delete_score
    
    #Delete awards data
    for i in awards_list:
        awards_data[i] = False
        
    with open("Achievements.txt", 'w') as awards:
        awards.write(str(awards_data))
        awards.close()
    
    #Delete options data
    pref_dict['Japanese'] = False
    pref_dict['Challenge'] = False
    pref_dict['Volume'] = 100.0
    
    with open("PlayerPreferences.txt", 'w') as prefs:
        prefs.write(str(pref_dict))
        prefs.close()
    
    #Delete Scoreboard Data
    score_dict = {}
    time_stamp = str(dt.datetime.now())
    score_dict[0] = "No_Player, 0"
    delete_score = True
        
    with open("Scoreboard.txt", 'w') as score:
        score.write(str(score_dict))
    
    Main_Menu()
        
#Applying options to prefs and writing to file
def apply_prefs(data):
    pref_dict['Challenge'] = data[0]
    pref_dict['Volume'] = data[1]
    
    with open("PlayerPreferences.txt", 'w') as prefs:
        prefs.write(str(pref_dict))
        prefs.close()
    
    Main_Menu()
        
#Function that prompts player for their name
def set_solo():
    global player1
    window = make_window('pn')
    
    event, values = window.read()
    
    if event == 'Enter':
        window.close()
        player1 = values[0]
        round_picker()
    else:
        window.close()
        Main_Menu()
        
#Function that prompts player for the amount of rounds
def round_picker():
    global first_round
    global round_limit
    window = make_window('r')
    
    event, values = window.read()
    
    first_round = True
    
    if event == 'Enter':
        round_limit = values[0]
        int(round_limit)
        window.close()
        question_type()
    else:
        window.close()
        set_solo()
    
#Big function that does most of the heavy lifting for game logic and calling the question to be asked
def question_type():
    global display_image
    global options
    global round
    global answer
    global round_limit
    global streak
    global player_score
    global jp_text
    global song_text
    global awards_data
    global first_round
    
    choice = ''
    
    #Clears previous question options
    options.clear()
    
    #Checks if player lost streak, if not sees if player has a new achievement
    if streak == 0:
        if not first_round:
            miku_message('You lost your streak....', 'whoa')
        else:
            miku_message("Good Luck!", 'goodluck')
            first_round = False
        player_score = player_score
    else:
        if streak == 5:
            if not awards_data['5streak'] == True:
                awards_data['5streak'] = True
                display_award('5streak')
        if streak == 10:
            if not awards_data['10streak'] == True:
                awards_data['10streak'] = True
                display_award('10streak')
        if streak == 25:
            if not awards_data['25streak'] == True:
                awards_data['25streak'] = True
                display_award('25streak')
        if streak == 50:
            if not awards_data['Legend'] == True:
                awards_data['Legend'] = True
                display_award('Legend')
                
        #Adds score    
        player_score += 25 * streak
    
    #Checks if over round limit
    if round < round_limit:
        round += 1
        
        #Checks for challenge option, executes a random type of question based of it
        if pref_dict['Challenge'] == True:
            decide = random.randint(0, 6)
            choice = game_type[decide]
        
        else:
            decide = random.randint(0, 5)
            choice = game_type[decide]
        
        #Image Question : Explains process of every other question option
        if choice == 'image':
        
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Name'][ran_int]
            display_image = game_data['Image'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(songs_list) -1)
                
                #Checks if ran_int2 is equal to any current options, prevents duplicate answers
                while ran_int == ran_int2 or [i for i in options if i == game_data["Name"][ran_int2]]:
                    ran_int2 = random.randint(0, len(songs_list) -1)

                options.append(game_data['Name'][ran_int2])
            
            #Inserts actual answer into a random location
            options.insert(random.randint(0, 4), game_data['Name'][ran_int])
            
            ask_question('image')
        
        #Japanese Title Question
        elif choice == 'japanese':
            
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Name'][ran_int]
            jp_text = game_data['Japanese'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(songs_list) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == game_data["Name"][ran_int2]]:
                    ran_int2 = random.randint(0, len(songs_list) -1)

                options.append(game_data['Name'][ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Name'][ran_int])
            
            ask_question('title')
        
        #Singer Question
        elif choice == 'singer':
            vocaloids = []
            for i in game_data['Singer']:
                vocaloids.append(i)
            
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Singer'][ran_int]
            song_text = game_data['Name'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(vocaloids) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == vocaloids[ran_int2]] or answer == vocaloids[ran_int2]:
                    ran_int2 = random.randint(0, len(vocaloids) -1)

                options.append(vocaloids[ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Singer'][ran_int])
            
            ask_question('singer')
        
        #Producer Question
        elif choice == 'producer':
            producer_list = []
            for i in game_data['Producer']:
                producer_list.append(i)

            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Producer'][ran_int]
            song_text = game_data['Name'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(producer_list) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == producer_list[ran_int2]] or answer == producer_list[ran_int2]:
                    ran_int2 = random.randint(0, len(producer_list) -1)

                options.append(producer_list[ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Producer'][ran_int])
            
            ask_question('producer')
        
        #Song 1 Question
        elif choice == 'sample1':
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Name'][ran_int]
            play_song = game_data['Sample 1'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(songs_list) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == game_data["Name"][ran_int2]]:
                    ran_int2 = random.randint(0, len(songs_list) -1)

                options.append(game_data['Name'][ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Name'][ran_int])
            
            sound_question(play_song)
        
        #Song 2 Question
        elif choice == 'sample2':
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Name'][ran_int]
            play_song = game_data['Sample 2'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(songs_list) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == game_data["Name"][ran_int2]]:
                    ran_int2 = random.randint(0, len(songs_list) -1)

                options.append(game_data['Name'][ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Name'][ran_int])
            
            sound_question(play_song)
        
        #Song 3 Question
        elif choice == 'sample3':
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Name'][ran_int]
            play_song = game_data['Sample 3'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(songs_list) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == game_data["Name"][ran_int2]]:
                    ran_int2 = random.randint(0, len(songs_list) -1)

                options.append(game_data['Name'][ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Name'][ran_int])
            
            sound_question(play_song)
    
    #If the limit has been reached, this code executes 
    else:
        #Displays amount of points that the user got
        if player_score == 0:
            miku_message('You got ' + str(player_score) + 'pts', 'sorry')
        else:
            miku_message('You got ' + str(player_score) + 'pts', 'greatshow')
        
        #Checks for if the user obtained achievements
        if round_limit == 50.0:
            if not awards_data['LongRound']:
                awards_data['LongRound'] = True
                display_award('LongRound')
        if round_limit == 1.0:
            if not awards_data["ShortRound"] == True:
                awards_data["ShortRound"] = True
                display_award('ShortRound')
        if player_score == 0:
            if not awards_data['0'] == True:
                awards_data['0'] = True
                display_award('0')
                
        #Saves Score
        save_score(player1, player_score)
        
        #Resets Variables
        streak = 0
        player_score = 0
        round = 0
        Main_Menu()

#Window for displaying award when collected
def display_award(name):
    global award_title
    
    if name == '5streak':
        award_title = '5 Streak'
    elif name == '10streak':
        award_title = '10 Streak'
    elif name == '25streak':
        award_title = '25 Streak'
    elif name == '0':
        award_title = "0 Points, Skill Issue"
    elif name == 'LongRound':
        award_title = '50 Rounds!'
    elif name == 'ShortRound':
        award_title = '1 Round!'
    elif name == 'Legend':
        award_title = "LEGEND"
        
    window = make_window('aw')
    
    event, values = window.read()
    
    window.close()
    
#Makes a window with the question type and handles streak amount            
def ask_question(type):
    global streak
    
    if type == 'image':
        window = make_window('im')
    elif type == 'title':
        window = make_window('tq')
    elif type == 'singer':
        window = make_window('sq')
    elif type == 'producer':
        window = make_window('pq')
    
    event, values = window.read()
    
    if event == answer:
        window.close()
        streak += 1
        question_type()
    else:
        window.close()
        streak = 0
        question_type()
        
#Makes a question window with sound in it and handles all logic around playing/stopping sound        
def sound_question(play_song):
    global streak
    
    p = ap('songs/' + play_song)
    p.volume = pref_dict["Volume"]
    
    window = make_window('sound_q')
    
    while True:
        event, values = window.read()
        
        if event == answer:
            p.stop()
            window.close()
            streak += 1
            question_type()
            break
        elif event == 'Play':
            p.play(block=False)
        elif event == 'Stop':
            p.stop()
        else:
            p.stop()
            window.close()
            streak = 0
            question_type()
            break
        
#Function for saving score and achievements
def save_score(name, score_num):
    global delete_score
    global score_dict
    with open("Achievements.txt", 'w') as awards:
        awards.write(str(awards_data))
        awards.close()
    
    time_stamp = str(dt.datetime.now())
    score_dict[time_stamp] = {"name": name, "score": score_num, "date": time_stamp}
    
    with open("Scoreboard.txt", 'w') as score:
        score.write(str(score_dict))
                
Main_Menu()