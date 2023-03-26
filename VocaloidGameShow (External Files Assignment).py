###########################################################
#External Files Assignment - Vocaloid Game Show
#CaptainKirby
#March 25, 2023
###########################################################

#Credits
#https://www.pysimplegui.org/en/latest/
#https://www.w3schools.com/python/module_random.asp

#Importing
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
score_text = ''
top3_text = ''

#Fail Safe Function
def default_files(type):
    global delete_score
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
            
def write_songs():
    temp_list = []
    for i in game_data['Name']:
        temp_list.append(i)
    return temp_list

#Opens and writes data from files to variables to be used later
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
        score.close()
        delete_score = False

except:
    with open("Scoreboard.txt", 'w') as score:
        default_files('s')
        delete_score = True
        score.close()

try:
    with open("Achievements.txt", 'r') as awards:
        #awards_data = eval(awards.read()) #Do once achievements are set
        awards.close()
        
except:
    with open("Achievements.txt", 'w') as awards:
        default_files('c')
        #Fix later, adding in support for all achievements to be set to False

try:
    game_data = pd.read_csv("vocaloid_data.csv")
    
except:
    print("The vocaloid_data.csv file is missing! Download from, https://docs.google.com/spreadsheets/d/1sg6z-Ixtalpy9ATyyEjjnqT2L-91g22pV_6xrKKFANw/edit?usp=sharing and put into the game folder")
    
songs_list = write_songs()
    
#Layout function, makes windows to avoid tag conflicts
def make_window(type):
    global options
    if type == "mm":
        main_menu = [ [sg.Push(), sg.Text("Welcome to the Vocaloid Quiz Game!", font=('times_new_roman', 24, 'bold')), sg.Push()],
                      [sg.Push(), sg.Image("images/TitleImage.png", pad=(20)), sg.Push()],
                      [sg.Push(), sg.Button("Play", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Scoreboard", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Achievements", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Options", expand_x=True), sg.Push()],
                      [sg.Push(), sg.Button("Exit", expand_x=True), sg.Push()] ]
        
        return sg.Window("Main Menu", main_menu)
        
    elif type == 'op':
        options = [ [sg.Push(), sg.Text("Options", font=('times_new_roman', 18, 'bold'), pad=10), sg.Push()],
                    [sg.Push(), sg.Checkbox("Japanese Sounds", font=('times_new_roman', 12), default=pref_dict['Japanese']), sg.Push()],
                    [sg.Push(), sg.Checkbox("Challenge Questions", font=('times_new_roman', 12), pad=20, default=pref_dict['Challenge']), sg.Push()],
                    [sg.Push(), sg.Slider(range=(0, 100), default_value=pref_dict['Volume'], orientation='h'), sg.Push()],
                    [sg.Push(), sg.Text("Slider Changes The Volume",font=('times_new_roman', 12)), sg.Push()],
                    [sg.Push(), sg.Button("Clear Save Data", pad=30, expand_x=True), sg.Push()],
                    [sg.Push(), sg.Button("Apply"), sg.pin(sg.Button("Exit", expand_x=True)), sg.Push()] ]
        
        return sg.Window("Options", options)
    
    elif type == 'mode':
        mode = [ [sg.Push(), sg.Text("What mode would you like to play?", font=('times_new_roman', 12), pad=20), sg.Push()],
                 [sg.Button("Solo", size=20), sg.pin(sg.Button("Vs. Computer", size=20)), sg.pin(sg.Button("Back", size=20))] ]
        
        return sg.Window("Mode Select", mode)
    
    elif type == 'pn':
        player_name = [ [sg.Push(), sg.Text("What is your name?", font=('times_new_roman', 12), pad=20), sg.Push()],
                        [sg.Push(), sg.Input(pad=20), sg.Push()],
                        [sg.Push(), sg.Button("Enter", size=20), sg.pin(sg.Button("Exit", size=20)), sg.Push()] ]
        
        return sg.Window("Player Name", player_name)
    
    elif type == 'r':
        play_setup = [ [sg.Push(), sg.Slider(range=(1, 50), default_value=10, orientation='h'), sg.Push()],
                       [sg.Push(), sg.Text("Number of Rounds",font=('times_new_roman', 12)), sg.Push()],
                       [sg.Push(), sg.Button("Enter", size=20), sg.pin(sg.Button("Exit", size=20)), sg.Push()] ]
        
        return sg.Window("Round Picker", play_setup)
    
    elif type == 'im':
        image_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text("What is this song?", font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Image(source='images/' + display_image, pad=20), sg.Push()],
                           [sg.Push(), sg.Button(options[0], size=20), sg.pin(sg.Button(options[1], size=20)), sg.Push()],
                           [sg.Push(), sg.Button(options[2], size=20), sg.pin(sg.Button(options[3], size=20)), sg.Push()] ]
        
        return sg.Window("Game", image_question)
    
    elif type == 's':
        scoreboard = [ [sg.Push(), sg.Text("Scoreboard", font=('times_new_roman', 18, 'bold'), pad=10), sg.Push()],
                       [sg.Push(), sg.Text("Top 3 Scores", font=('times_new_roman', 16, 'bold'), pad=10), sg.Push()],
                       [sg.Push(), sg.Text(top3_text, font=('times_new_roman', 12), pad=10), sg.Push()],
                       [sg.Push(), sg.Text("Last 10 Scores", font=('times_new_roman', 16, 'bold'), pad=10), sg.Push()],
                       [sg.Push(), sg.Text(score_text, font=('times_new_roman', 12), pad=10), sg.Push()] ]
        
        return sg.Window("Scoreboard", scoreboard)
    
    elif type == 'tq':
        title_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text("What is this song?", font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text(jp_text, font=('times_new_roman', 18), pad=20), sg.Push()],
                           [sg.Push(), sg.Button(options[0], size=20), sg.pin(sg.Button(options[1], size=20)), sg.Push()],
                           [sg.Push(), sg.Button(options[2], size=20), sg.pin(sg.Button(options[3], size=20)), sg.Push()] ]
        
        return sg.Window("Game", title_question)
    
    elif type == 'sq':
        singer_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                            [sg.Push(), sg.Text("Who Sings " + song_text + "?", font=('times_new_roman', 12), pad=20), sg.Push()],
                            [sg.Push(), sg.Button(options[0], size=20), sg.pin(sg.Button(options[1], size=20)), sg.Push()],
                            [sg.Push(), sg.Button(options[2], size=20), sg.pin(sg.Button(options[3], size=20)), sg.Push()] ]
        
        return sg.Window("Game", singer_question)
        
    elif type == 'pq':
        producer_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                              [sg.Push(), sg.Text("Who Produced " + song_text + "?", font=('times_new_roman', 12), pad=20), sg.Push()],
                              [sg.Push(), sg.Button(options[0], size=20), sg.pin(sg.Button(options[1], size=20)), sg.Push()],
                              [sg.Push(), sg.Button(options[2], size=20), sg.pin(sg.Button(options[3], size=20)), sg.Push()] ]
        
        return sg.Window("Game", producer_question)
    
    elif type == 'sound_q':
        sound_question = [ [sg.Push(), sg.Text("Round " + str(round), font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Text("What is this song?", font=('times_new_roman', 12)), sg.Push()],
                           [sg.Push(), sg.Button("Play", pad=20), sg.pin(sg.Button("Stop", pad=20)), sg.Push()],
                           [sg.Push(), sg.Button(options[0], size=20), sg.pin(sg.Button(options[1], size=20)), sg.Push()],
                           [sg.Push(), sg.Button(options[2], size=20), sg.pin(sg.Button(options[3], size=20)), sg.Push()] ]
        
        return sg.Window("Game", sound_question)

#Main Menu Function
def Main_Menu():
    window = make_window('mm')
    
    event, values = window.read()
    
    if event == "Play":
        window.close()
        setup_play()
    elif event == "Scoreboard":
        window.close()
        scoreboard()
    elif event == "Achievements":
        #Do Fourth
        window.close()
        Main_Menu()
        print("Look at dem trophies! That you don't have :trol:")
    elif event == "Options":
        window.close()
        Options_Menu()
    else:
        window.close()

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
        
        if event == 'Exit':
            print("You broke this somehow")
        else:
            window.close()
            Main_Menu()
            
    else:
        del score_dict[0]
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
    else:
        Main_Menu()
        window.close()
        
#Applying options to prefs and writing to file
def apply_prefs(data):
    pref_dict['Japanese'] = data[0]
    pref_dict['Challenge'] = data[1]
    pref_dict['Volume'] = data[2]
    
    with open("PlayerPreferences.txt", 'w') as prefs:
        prefs.write(str(pref_dict))
        prefs.close()
    
    Main_Menu()
    
def setup_play():
    window = make_window('mode')
    
    event, values = window.read()
    
    if event == 'Solo':
        window.close()
        set_solo()
    else:
        window.close()
        Main_Menu()
        
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
        setup_play()
        
def round_picker():
    global round_limit
    window = make_window('r')
    
    event, values = window.read()
    
    if event == 'Enter':
        round_limit = values[0]
        int(round_limit)
        window.close()
        question_type()
    else:
        window.close()
        set_solo()
    
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
    
    options.clear()
    if streak == 0:
        player_score = player_score
    else:
        player_score += 25 * streak 
    if round < round_limit:
        round += 1
    
        if pref_dict['Challenge'] == True:
            decide = random.randint(0, 6)
            choice = game_type[decide]
        
        else:
            choice = random.randint(0, 5)
            print(game_type[choice])
        
        if choice == 'image':
        
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Name'][ran_int]
            display_image = game_data['Image'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(songs_list) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == game_data["Name"][ran_int2]]:
                    ran_int2 = random.randint(0, len(songs_list) -1)

                options.append(game_data['Name'][ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Name'][ran_int])
            
            image_question()
            
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
            
            title_question()
            
        elif choice == 'singer':
            vocaloids = ['Miku', 'Rin', 'Len', 'Kaai Yuki', 'Vivid BAD Squad', 'Eve', 'Gumi', 'Luka', 'Kaito'] #CHANGE LATER ONCE MORE SINGERS ARE IN THE GAME
            
            ran_int = random.randint(0, len(songs_list) -1)
            answer = game_data['Singer'][ran_int]
            song_text = game_data['Name'][ran_int]
        
            for i in range(3):
                ran_int2 = random.randint(0, len(vocaloids) -1)
                
                while ran_int == ran_int2 or [i for i in options if i == vocaloids[ran_int2]] or answer == vocaloids[ran_int2]:
                    ran_int2 = random.randint(0, len(vocaloids) -1)

                options.append(vocaloids[ran_int2])
                
            options.insert(random.randint(0, 4), game_data['Singer'][ran_int])
            
            singer_question()
            
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
            
            producer_question()
            
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
            
    else:
        print('GAME ENDED')
        save_score(player1, player_score)
        streak = 0
        player_score = 0
        round = 0
        Main_Menu()
        
def image_question():
    global streak
    
    window = make_window('im')
    
    event, values = window.read()
    
    if event == answer:
        print('CORRECT')
        window.close()
        streak += 1
        question_type()
    else:
        print("WRONG")
        window.close()
        streak = 0
        question_type()
        
def title_question():
    global streak
    
    window = make_window('tq')
    
    event, values = window.read()
    
    if event == answer:
        print('CORRECT')
        window.close()
        streak += 1
        question_type()
    else:
        print("WRONG")
        window.close()
        streak = 0
        question_type()
        
def singer_question():
    global streak
    
    window = make_window('sq')
    
    event, values = window.read()
    
    if event == answer:
        print('CORRECT')
        window.close()
        streak += 1
        question_type()
    else:
        print("WRONG")
        window.close()
        streak = 0
        question_type()
        
def producer_question():
    global streak
    
    window = make_window('pq')
    
    event, values = window.read()
    
    if event == answer:
        print('CORRECT')
        window.close()
        streak += 1
        question_type()
    else:
        print("WRONG")
        window.close()
        streak = 0
        question_type()
        
def sound_question(play_song):
    global streak
    
    p = ap('songs/' + play_song)
    p.volume = pref_dict["Volume"]
    
    window = make_window('sound_q')
    
    while True:
        event, values = window.read()
        
        if event == answer:
            print('CORRECT')
            window.close()
            streak += 1
            question_type()
            break
        elif event == 'Play':
            p.play(block=False)
        elif event == 'Stop':
            p.stop()
        else:
            print("WRONG")
            window.close()
            streak = 0
            question_type()
            break
        
def save_score(name, score_num):
    global delete_score
    if delete_score:
        del score_dict[0]
        delete_score = False
        time_stamp = str(dt.datetime.now())
        score_dict[time_stamp] = {"name": name, "score": score_num, "date": time_stamp}
        
        with open("Scoreboard.txt", 'w') as score:
            score.write(str(score_dict))
    else:
        time_stamp = str(dt.datetime.now())
        score_dict[time_stamp] = {"name": name, "score": score_num, "date": time_stamp}
        
        with open("Scoreboard.txt", 'w') as score:
            score.write(str(score_dict))
                
Main_Menu()