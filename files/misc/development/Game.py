'''Triva Program Code Package (4/4)'''

'''Code for button and data functionallity of Triva Program
Contains functionality for saving data in each game and interfacing with buttons'''

import pygame
import random
import os
from datetime import datetime
from pandas import read_excel,read_csv

class Game():
    '''Contains information relating the players, scores, and buttons'''
    def __init__(self):
        '''Create game object'''
        pygame.init()
        self.S = Settings()
        self.M = Music(self)
        self.A = Alarm(self)
        self.P = {} # Players
        self.B = [] # Question Boards
        self.H = [] # History
        self.F = Files()
        self.reconnect()
    def new(self,file):
        '''Load data from question file'''
        self.F.file = file
        self.H.append('Loaded: {}'.format(os.path.basename(file)))
        self.B = []
        if file[-3:] == 'csv':
            data = read_csv(file,keep_default_na=False)
        elif file[-4:] == 'xlsx':
            data = read_excel(file,keep_default_na=False)
        else:
            return
        for index,row in data.iterrows():
            try:
                b = [B.name for B in self.B].index(row[0])         
            except ValueError:
                if row[0] != '':
                    self.B.append(Board(row[0]))
                    b = len(self.B)-1
                    last_b = b
                else:
                    b = last_b
            # Find Category
            try:
                c = [C.name for C in self.B[b].C].index(row[1])         
            except ValueError:
                if row[1] != '':
                    self.B[b].C.append(Category(row[1],row[2]))
                    c = len(self.B[b].C)-1
                    last_c = c
                else:
                    c = last_c
            # Add Questions
            if row[3] != '':
                self.B[b].C[c].Q.append(Question(row[3],row[4],row[5],row[6],row[7]))
    def reconnect(self):
        '''Refresh connected controllers'''
        pygame.joystick.quit()
        pygame.joystick.init()
        self.J = pygame.joystick.get_count()
    def buzz(self):
        '''Test buttons pressed'''
        num = []
        pygame.event.pump()
        # for every contoller
        for j in range(self.J):
            J = pygame.joystick.Joystick(j)
            J.init()
            # for every button
            for b in range(J.get_numbuttons()):
                if J.get_button(b) != 0:
                    num.append(str(j)+'b'+str(b))
            # for every hat
            for h in range(J.get_numhats()):
                # for each dimension
                for i in range(len(J.get_hat(h))):
                    if J.get_hat(h)[i] != 0:
                        num.append(str(j)+'h'+str(h)+'i'+str(i)+'d'+str(J.get_hat(h)[i]))
        return num
    def add(self,num,name):
        '''Add a new player via button information'''
        self.P[num] = Player(name) 
    def ordered(self):
        '''Make list of players ordered by score'''
        nums = list(self.P.keys())
        scores = [self.P[n].points for n in nums]
        return [num for _,num in sorted(zip(scores,nums),reverse=True)]
    def check_files(self):
        '''check if image/music folder has all required files'''
        missing_files = []
        for B in self.B:
            for C in B.C:
                for Q in C.Q:
                    for file in Q.files:
                        try:
                            if not(file in os.listdir(self.F.folder)):
                                missing_files.append(file)
                        except:
                            missing_files.append(file)
        return missing_files
    def reset_settings(self):
        self.S = Settings()
    def save(self):
        if len(self.H) > 0:
            try: 
                name = datetime.now().strftime('files\logs\%y-%m-%d__%H-%M.txt')
                with open(name,'w') as f:
                    f.write('--------- Scores ---------\n')
                    for p in self.ordered():
                        name = self.P[p].name
                        points = self.P[p].points
                        f.write('{:15s} {}\n'.format(name,points))
                    f.write('---------- Log -----------\n')
                    f.write("\n".join(self.H)) 
            except: pass
                    
    def quit(self):
        pygame.quit()
        
class Player():
    '''Player Class
    @param name Name assigned to a button
    @param points Number if points assigned to a button'''
    def __init__(self,name):
        self.name = name
        self.points = 0
class Board():
    '''Board Class
    @param name Name of board
    @param C List of categories'''
    def __init__(self,name):
        self.name = name
        self.C = []
class Category():
    '''Category Class
    @param name Name of category
    @param description Description of category
    @param Q List of questions'''
    def __init__(self,name,description):
        self.name = name
        self.descript = description
        self.Q = []
class Question():
    '''Question Class
    @param point Point Value
    @param text Question Text
    @param answer Answer Text
    @param time Extra time for question
    @param file Image or music file for question'''
    def __init__(self,points,text,answer,time,files):
        self.points     = int(points)
        self.text       = text
        self.answer     = answer
        try:
            self.time   = int(time)
        except:
            self.time   = 0
        files           = [f.strip() for f in files.split(',')]
        if '' in files: files.remove('')
        self.files = files

class Files():
    def __init__(self):
        self.file = None
        self.folder = None
        
class Settings():        
    '''Settings information'''
    def __init__(self):
        self.multi_guess = True
        self.timer_bar = True
        self.timer_txt = True
        self.alarm_vol = 50
        self.music_vol = 50
        self.timer_question = 10
        self.timer_response = 5
        self.timer_answer = 5
        self.color_bg = '#004713'
        self.color_bg_dark = '#002d0c'
        self.color_bg_light = '#00661c'
        self.color_txt = '#d8d8d8'
        self.color_timer = 'red2'           
        
class Music():
    '''Musics for question'''
    def __init__(self,game):
        '''Start pygame functionality'''
        pygame.mixer.init()
        self.on = False
        self.game = game
    def play(self,file):
        '''Play a music file'''
        pygame.mixer.music.set_volume(self.game.S.music_vol/100)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        self.on = True
    def pause(self):
        '''Pause the music'''
        if self.on:
            pygame.mixer.music.pause()
    def unpause(self):
        '''Unpause the music'''
        if self.on:
            pygame.mixer.music.unpause()
    def stop(self):
        '''Stop the music'''
        if self.on:
            pygame.mixer.music.stop()
            self.on = False

class Alarm():
    '''Controls sound effects'''
    def __init__(self,game):
        '''Load in file locations for sound effects'''
        d = os.path.abspath(r"files\sounds\alarm")
        self.alarm = [os.path.join(d,f) for f in os.listdir(d)]
        d = os.path.abspath(r"files\sounds\correct")
        self.correct = [os.path.join(d,f) for f in os.listdir(d)]
        d = os.path.abspath(r"files\sounds\incorrect")
        self.incorrect = [os.path.join(d,f) for f in os.listdir(d)]
        d = os.path.abspath(r"files\sounds\ding")
        self.ding = [os.path.join(d,f) for f in os.listdir(d)]
        self.game = game
    def play(self,i):
        '''Play a random sound for type selected'''
        pygame.mixer.stop()
        if   i=='a' : self.sound = pygame.mixer.Sound(random.choice(self.alarm))
        elif i=='c' : self.sound = pygame.mixer.Sound(random.choice(self.correct))
        elif i=='i' : self.sound = pygame.mixer.Sound(random.choice(self.incorrect))
        elif i=='d' : self.sound = pygame.mixer.Sound(random.choice(self.ding))
        else: self.sound = pygame.mixer.Sound(os.path.abspath(self.game.F.folder+i))
        self.sound.set_volume(self.game.S.alarm_vol/100)
        pygame.mixer.Sound.play(self.sound)
    def stop(self):
        '''Stop playing sound'''
        pygame.mixer.stop()     

'''Runs Program if File is clicked'''  
if __name__ == "__main__":
    from TriviaProgram import MainWindow       
    main = MainWindow()
    main.mainloop()
