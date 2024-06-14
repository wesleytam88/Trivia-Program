'''Triva Program Code Package (3/4)'''

'''Code for controller question of Triva Program
Contains functionality for running a question'''

import tkinter as tk
from PIL import Image, ImageTk
import os
import time
import random
import cv2

class C_Question(tk.Frame):
    '''Controller question screen providing all relavent details'''
    def __init__(self,cont,main,game):
        '''Create Frame'''
        tk.Frame.__init__(self,cont.frame)
        # Load in data to acccess in functions
        self.cont = cont
        self.main = main
        self.game = game
        # Set up Question Bar
        self.S1 = tk.Frame(self)
        tk.Label(self.S1,text="Category:",justify='left').grid(row=0,column=0)
        self.category = tk.Label(self.S1,text="",justify='left')
        self.category.grid(row=0,column=1,sticky='w')
        tk.Label(self.S1,text="Question:",justify='left').grid(row=1,column=0)
        self.question = tk.Label(self.S1,text="",justify='left')
        self.question.grid(row=1,column=1,sticky='w')
        tk.Label(self.S1,text="Answer:",justify='left').grid(row=2,column=0)
        self.answer = tk.Label(self.S1,text="",justify='left')
        self.answer.grid(row=2,column=1,sticky='w')
        self.S1.grid_rowconfigure([0,1,2],weight=1)
        self.S1.grid_columnconfigure([0,1],weight=1)
        self.S1.grid(row=0,column=0,sticky="nsew")               
        # Set up basic controles
        self.S2 = tk.Frame(self)
        self.btn0 = tk.Button(self.S2,text="Pause",command=self.pause1,bd=4,background='gray25',width=15)
        self.btn0.grid(row=0,column=0)
        self.btn1 = tk.Button(self.S2,text="End",command=self.end,bd=4,background='gray25',width=15)
        self.btn1.grid(row=0,column=1)
        self.timer = tk.Label(self.S2,text="")
        self.timer.grid(row=1,column=0,columnspan=2,sticky='nsew')
        self.S2.grid_rowconfigure([0,1],weight=1)
        self.S2.grid_columnconfigure([0,1],weight=1)
        self.S2.grid(row=1,column=0,sticky="nsew")
        # Set up Player Bar
        self.S3 = tk.Frame(self)
        self.player = tk.Label(self.S3,text="Player")
        self.player.grid(row=0,column=0,columnspan=3,sticky='nsew')
        tk.Button(self.S3,text="Correct",command=self.correct,bd=4,background='gray25',width=15).\
            grid(row=1,column=0)
        tk.Button(self.S3,text="Incorrect",command=self.incorrect,bd=4,background='gray25',width=15).\
            grid(row=1,column=1)
        tk.Button(self.S3,text="Cancel",command=self.cancle,bd=4,background='gray25',width=15).\
            grid(row=1,column=2)        
        self.S3.grid_rowconfigure([0,1],weight=1)
        self.S3.grid_columnconfigure([0,1,2],weight=1)
        self.S3.grid(row=2,column=0,sticky="nsew")        
        # Combines
        self.grid_rowconfigure([0,1,2],weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid(row=0,column=0,sticky="nsew")
    def run(self,b,c,q,temp=False):
        '''Start Question and load new info'''
        # Start Question
        game = self.game
        game.A.stop()
        width = self.winfo_width()
        self.category.config(text=game.B[b].C[c].name,wrap=width*.5)
        self.question.config(text=game.B[b].C[c].Q[q].text,wrap=width*.5)
        self.answer.config(text=game.B[b].C[c].Q[q].answer,wrap=width*.5)
        self.S3.grid_remove()
        play_video = False
        self.tkraise()
        screen = self.main.question
        screen.category.config(text=game.B[b].C[c].name)
        if game.B[b].C[c].Q[q].text != '':
            screen.question.config(text=game.B[b].C[c].Q[q].text)
            screen.question.grid()
        else:
            screen.question.grid_remove()
        # load media
        files = game.B[b].C[c].Q[q].files
        videos = [f for f in files if f.split('.')[-1] in {'mp4','avi'}]
        music  = [f for f in files if f.split('.')[-1] in {'wav','mp3'}]
        images = [f for f in files if f.split('.')[-1] not in {'avi','mp4','wav','mp3'}]
        screen.image.grid_remove()
        if len(videos) > 0:
            try:
                file = os.path.join(game.F.folder,videos[0])
                if len(images) == 0:
                    play_video = True
                    video = cv2.VideoCapture(file)
                    w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
                    h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
                    scale = self.main.height/h*.6
                    self.w = int(w*scale)
                    self.h = int(h*scale)
                    _, frame = video.read()
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img,(self.w,self.h))
                    screen.pic = ImageTk.PhotoImage(Image.fromarray(img))
                    screen.image.config(image=screen.pic)
                    screen.image.grid()
            except: pass
            
        if len(images) > 0 :
            try:
                file = os.path.join(game.F.folder,images[0]) 
                pic = Image.open(file)
                scale = self.main.height/pic.height*.6
                h = int(pic.height*scale)
                w = int(pic.width*scale)
                screen.pic = ImageTk.PhotoImage(pic.resize((w,h),Image.ANTIALIAS))
                screen.image.config(image=screen.pic)
                screen.image.grid()                
            except: pass
        
        if len(music) > 0:
            try:
                file = os.path.join(game.F.folder,music[0]) 
                game.M.play(file)
            except: pass
        
        screen.tkraise()
        # Wait for Buzz           
        self.state = False
        self.stop = False
        guessed_nums = set()
        q_del_time = game.S.timer_question + game.B[b].C[c].Q[q].time
        q_final_time = time.time() + q_del_time
        while not(self.state):
            q_rem_time = q_final_time - time.time()
            self.timer.config(text="{:.0f}".format(q_rem_time))
            screen.timer.update(q_rem_time,q_del_time)
            if self.stop:
                self.main.text.update('Game Paused')
                self.pause2()
                screen.tkraise()
                q_final_time = time.time() + q_rem_time
            if play_video:
                vid_time = int((q_del_time-q_rem_time)*1000)
                video.set(cv2.CAP_PROP_POS_MSEC,vid_time)
                _, frame = video.read()
                if frame is not None:
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img,(self.w,self.h))
                    screen.pic = ImageTk.PhotoImage(Image.fromarray(img))
                    screen.image.config(image=screen.pic)
            self.main.update()
            self.main.update_idletasks()
            try:
                num = random.choice(list(set(game.buzz())&set(game.P.keys())-guessed_nums))
                game.M.pause()
                game.A.play('d')
                self.player.config(text=game.P[num].name)
                self.S3.grid()
                screen = self.main.player
                screen.name.config(text='')
                screen.name.grid()
                screen.label.config(text=game.P[num].name)
                screen.timer.grid()
                screen.tkraise()
                a_del_time = game.S.timer_response
                a_final_time = time.time() + a_del_time                
                self.state = False
                # Wait for Ruling
                while not(self.state):
                    a_rem_time = a_final_time-time.time()
                    self.timer.config(text="{:.0f}".format(a_rem_time))
                    screen.timer.update(a_rem_time,a_del_time)
                    self.main.update()
                    self.main.update_idletasks()
                    if self.stop:
                        self.main.text.update('Game Paused')
                        self.pause2()
                        screen.tkraise()
                        a_final_time = time.time() + a_rem_time
                    if time.time() > a_final_time:
                        self.main.text.update('Time is Up\nPlease Make Your Guess')
                        game.A.play('a')
                        break
                while not(self.state):
                    self.main.update()
                    self.main.update_idletasks() 
                self.S3.grid_remove()
                if self.val == 1:
                    game.A.play('c')
                    game.P[num].points += game.B[b].C[c].Q[q].points
                    game.H.append('{:15s} +{} [b{} c{} q{}]'.\
                        format(game.P[num].name,game.B[b].C[c].Q[q].points,b,c,q))
                    if game.S.multi_guess == 0:
                        guessed_nums.add(num) 
                elif self.val == -1:
                    game.A.play('i')
                    game.P[num].points -= game.B[b].C[c].Q[q].points
                    game.H.append('{:15s} -{} [b{} c{} q{}]'.\
                        format(game.P[num].name,game.B[b].C[c].Q[q].points,b,c,q))
                    self.state = False
                    if game.S.multi_guess == 0:
                        guessed_nums.add(num) 
                else:
                    game.A.stop()
                    self.state = False  
                game.M.unpause()
                screen = self.main.question
                screen.tkraise()
                q_final_time = time.time() + q_rem_time
            except IndexError:
                pass
            if time.time() > q_final_time:
                game.A.play('a')
                break            
        # Question Over
        game.M.stop()
        if not(temp):
            tk.Label(self.main.board.S1,text="",bg=self.game.S.color_bg_dark).grid(row=q+1,column=c,sticky="nesw")
            tk.Label(self.cont.board.S1,text="",bg='black').grid(row=q+1,column=c,sticky="nesw") 
            self.cont.board.count -= 1
        screen = self.main.answered.new(game.B[b].C[c].Q[q].answer)
        self.state = False
        self.stop = False
        rem_time = game.S.timer_answer
        end_time = rem_time + time.time()
        while True:
            if self.stop:
                self.pause2()
                end_time = rem_time + time.time()
            else:
                rem_time = end_time - time.time()
            if rem_time < 0: break
            if self.state:  break
            self.timer.config(text="{:.0f}".format(rem_time))
            self.main.update()
            self.main.update_idletasks()

                
        game.A.stop()
        # Check if board is empty
        if self.cont.board.count <= 0:
            if not(temp):
                b += 1
                if b >= len(game.B):
                    self.main.scores.label.config(text='Final Scores')
                    self.main.scores.new()
                    game.H.append('Game Finished')
                    self.cont.advanced.tkraise()
                else:
                    self.cont.board.new(b)
            else:
                self.main.scores.new()
                self.cont.advanced.tkraise()
        else:
            self.cont.board.tkraise()
            self.main.board.tkraise()
            
    def correct(self):
        '''Correct answer was given'''
        self.state = True
        self.val = 1
    def incorrect(self):
        '''Incorrect answer was given'''
        self.state = True
        self.val = -1
    def cancle(self):
        '''Cancel button press'''
        self.state = True
        self.val = 0
    def end(self):
        '''Stop Question'''
        self.val = 0
        self.state = True
    def pause1(self):
        '''Game to be paused'''
        self.stop = True
    def pause2(self):
        '''Game paused'''
        self.game.A.stop()
        self.game.M.pause()
        self.go = False
        self.btn0.config(text='Resume',command=self.resume)
        while not(self.go):
            self.main.update()
            self.main.update_idletasks()
        self.btn0.config(text='Pause',command=self.pause1)   
        self.game.M.unpause()
        self.stop = False
    def resume(self):
        '''Game resumed'''
        self.go = True

'''Runs Program if File is clicked'''        
if __name__ == "__main__":
    from TriviaProgram import MainWindow       
    main = MainWindow()
    main.mainloop()