'''Triva Program Code Package (2/4)'''

'''Code for controller of Triva Program, refered to as cont in the code
Contains most functionality except for running a question'''

import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor        
from functools import partial
from Question import C_Question
import pickle

class Controller(tk.Toplevel):
    '''Controller Window'''
    def __init__(self,main,game):
        '''Creates controller window and all frames'''
        tk.Toplevel.__init__(self,main)
        self.iconbitmap(r"./files/misc/icon.ico")
        self.title("Controller")
        self.protocol("WM_DELETE_WINDOW", lambda:self.on_closing(main,game))
        self.lift()
        self.frame = tk.Frame(self)
        self.frame.pack(side="top",fill="both",expand=True)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_columnconfigure(0,weight=1)
        # Other pages
        self.start = C_Start(self,main,game)
        self.board = C_Board(self,main,game)
        self.question = C_Question(self,main,game)
        self.players = C_Players(self,main,game)
        self.advanced = C_Advanced(self,main,game)
        self.board_select = C_Board_Select(self,main,game)
        self.quest_select = C_Quest_Select(self,main,game)
        self.category = C_Category(self,main,game)
        self.settings = C_Settings(self,main,game)
        self.colors = C_Colors(self,main,game)
        self.file = C_File(self,main,game)
        self.start.tkraise()
    def on_closing(self,main,game):
        '''Quits'''
        temp = Confirm(self,main,"Are you sure you want to quit","Yes","No")
        if temp.wait():
            game.save()
            game.quit()
            main.destroy()
        temp.destroy()
        self.lift()
                    
class C_Start(tk.Frame):
    '''Gives option to loads question data and adding players'''
    def __init__(self,cont,main,game):
        '''Creates Frame'''
        self.cont = cont
        self.main = main 
        self.game = game
        tk.Frame.__init__(self,cont.frame)
        tk.Button(self,text="Add Players",command=self.add_players,\
            bd=4,background='gray25',width=15).grid(row=0,column=0)
        tk.Button(self,text="Select Files",command=self.new_game,\
            bd=4,background='gray25',width=15).grid(row=1,column=0)
        tk.Button(self,text="How to Play",command=self.how_play,\
            bd=4,background='gray25',width=15).grid(row=2,column=0)
        self.grid_rowconfigure([0,1,2],weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid(row=0,column=0,sticky="nsew")
    def new_game(self):
        '''Moves to new game frame'''
        self.cont.file.tkraise()
    def add_players(self):
        '''Moves to add player frame'''
        self.cont.players.new()
    def how_play(self):
        '''Opens Help Text'''
        How2Play(self.cont)            
        
class C_Board(tk.Frame):
    '''Question selection screen during game'''
    def __init__(self,cont,main,game):
        '''Create Frame'''
        tk.Frame.__init__(self,cont.frame)
        # Load in data to acccess in functions
        self.cont = cont
        self.main = main 
        self.game = game
        # Creat main layout of Grid + Bottom Button
        self.S1 = tk.Frame(self)
        self.S1.grid(row=0,column=0,columnspan=3,sticky="nsew")
        tk.Button(self,text="Players",command=self.players,bd=4,background='gray25').grid(row=1,column=0,sticky="nsew")
        tk.Button(self,text="Advanced",command=self.advanced,bd=4,background='gray25').grid(row=1,column=1,sticky="nsew")
        tk.Button(self,text="Settings",command=self.settings,bd=4,background='gray25').grid(row=1,column=2,sticky="nsew")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure([0,1,2],weight=1,uniform='cont')
        self.grid(row=0,column=0,sticky="nsew")
    def new(self,b):
        '''Load new baords for controller and screen'''
        self.S1.destroy()
        self.S1 = tk.Frame(self,bg='black')
        screen = self.main.board
        screen.S1.destroy()
        screen.S1 = tk.Frame(screen,bg=self.game.S.color_bg_dark)
        # Keep count of active questions
        self.count = 0
        # Get size of each box
        width = (screen.main.width/len(screen.game.B[b].C)-screen.pad*2)*.9
        height = (screen.main.height/(max([len(C.Q) for C in screen.game.B[0].C])+1)-screen.pad*2)*.9
        [_,q_pnts] = screen.main.test.font(str(self.game.B[b].C[0].Q[0].points),'Arial',width*.8,height*.8)
        # Itterate through each category
        c = 0
        for C in self.game.B[b].C:
            # Get formated category name that fits in cell
            [txt,pnts] = screen.main.test.font(C.name,'Arial',width,height)
            # Add category for controller
            tk.Button(self.S1,text=txt,justify='center',command=partial(self.category,b,c),relief='solid').\
                grid(row=0,column=c,sticky="nsew")
            self.S1.grid_columnconfigure(c,weight=1,uniform='cont')
            # Add category for screen
            tk.Button(screen.S1,text=txt,font=('Arial',pnts),relief='flat',fg=self.game.S.color_txt,bg=self.game.S.color_bg,\
                command=partial(self.category,b,c)).\
                grid(row=0,column=c,padx=screen.pad,pady=screen.pad,sticky="nsew")
            screen.S1.grid_columnconfigure(c,weight=1,uniform='screen')
            screen.S1.grid_rowconfigure(0,weight=1,uniform='screen')
            # Itterate through each question
            q = 0
            for Q in C.Q:
                # Add question for contoller                
                self.S1.grid_rowconfigure(q+1,weight=1)
                btn = tk.Button(self.S1,text=str(Q.points),command=partial(self.question,b,c,q),relief='solid')
                
                btn.grid(row=q+1,column=c,sticky="nsew")
                # Add question for screen
                screen.S1.grid_rowconfigure(q+1,weight=1,uniform='screen')
                btn = tk.Button(screen.S1,text=str(Q.points),relief='flat',font=('Arial',q_pnts,'bold'),fg=self.game.S.color_txt,bg=self.game.S.color_bg_light,\
                    command=partial(self.question,b,c,q))
                btn.grid(row=q+1,column=c,padx=screen.pad,pady=screen.pad,sticky="nsew")
                q += 1
                self.count += 1
            c += 1   
        # Pack the new grid sections and raise the screen
        self.S1.grid(row=0,column=0,columnspan=3,sticky="nsew")
        self.tkraise()
        screen.S1.grid(row=0,column=0,padx=screen.pad,pady=screen.pad,sticky="nsew")
        screen.tkraise()
    def question(self,b,c,q):
        '''Runs new question function'''
        self.cont.question.run(b,c,q)
    def category(self,b,c):
        '''Display category details'''
        self.cont.category.new(b,c)
    def players(self):
        '''Load player menu'''
        self.cont.players.new()
    def advanced(self):
        '''Load advanced menu'''
        self.cont.advanced.tkraise()
        self.main.text.update('Accessing Special Features')
    def settings(self):
        '''Load settings menu'''
        self.cont.settings.tkraise()
        self.main.text.update('Adjusting Settings')

class C_Players(tk.Frame):
    '''Allows user to add, remove, and adjust players'''
    def __init__(self,cont,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        self.S1 = tk.Frame(self)
        self.S1.grid(row=0,column=0,padx=15,pady=15)
        self.S1.grid_remove()
        self.S2 = tk.Frame(self)
        self.entry = tk.Entry(self.S2,bg='gray35')
        self.entry.bind("<Return>",self.enter_new)
        self.entry.grid(row=0,column=0,ipadx=10,pady=15,ipady=0,sticky='nse')
        self.btn = tk.Button(self.S2,text="Add",command=self.add,bd=4,background='gray25')
        self.btn.grid(row=0,column=1,ipadx=10,ipady=0,pady=15,sticky='nsw')
        tk.Button(self.S2,text="Refresh Devices",command=self.refresh,bd=4,background='gray25')\
            .grid(row=1,column=0,columnspan=2,ipadx=10,ipady=0,padx=20,pady=15) 
        tk.Button(self.S2,text="Done",command=self.done,bd=4,background='gray25')\
            .grid(row=2,column=0,columnspan=2,ipadx=10,ipady=0,padx=20,pady=15)
        self.S2.grid_columnconfigure([0,1],weight=1)
        self.S2.grid(row=0,column=1,sticky="nsew",padx=15,pady=15)
        self.grid_columnconfigure([0,1],weight=1)
        self.grid_rowconfigure([0],weight=1)
        self.grid(row=0,column=0,sticky="nsew")
    def new(self):
        '''Updates screen and buttons to show current players and scores'''
        self.S1.destroy()
        self.S1 = tk.Frame(self)
        self.scores = []
        self.names = []
        count = 0
        for p in self.game.ordered():
            name = tk.Entry(self.S1,bg='gray35')
            name.insert(0,str(self.game.P[p].name))
            name.grid(row=count,column=0,ipadx=10,ipady=0,sticky='nsew')
            name.bind("<Return>",self.enter_change)
            self.names.append(name)    
            score = tk.Entry(self.S1,width=10,justify='center',bg='gray35')
            score.insert(0,str(self.game.P[p].points))
            score.grid(row=count,column=1,ipadx=10,ipady=0,sticky='nsew')
            score.bind("<Return>",self.enter_change)
            self.scores.append(score)
            tk.Button(self.S1,text="X",command=partial(self.remove,p),bd=4,background='gray25')\
                .grid(row=count,column=2,ipadx=10,ipady=0,sticky='nsew')
            count += 1
        self.S1.grid(row=0,column=0,padx=15,pady=15,sticky='n')
        self.entry.delete(0,'end')
        if len(self.names) > 0:
            self.main.scores.new()
        else:
            self.main.text.update('Adding Players')
        self.tkraise()
        
    def enter_new(self,event):
        '''Goes to add'''
        self.add()
    def enter_change(self,event):
        '''Updates player values based on screen'''
        count = 0
        for p in self.game.ordered():
            name = self.names[count].get()
            # Save data to history file
            if name != self.game.P[p].name:
                self.game.H.append(self.game.P[p].name+' --> '+name)
                self.game.P[p].name = name
            score = eval(self.scores[count].get())
            if score != self.game.P[p].points:
                self.game.H.append('{:15s} {:+} [edit]'.format(name,score-self.game.P[p].points))
                self.game.P[p].points = score
            count += 1
        self.new()
        self.main.scores.new()
    def add(self):
        '''Adds new player'''
        name = self.entry.get()
        self.main.player.name.config(text=name)
        self.main.player.label.config(text="Please Hit Your Button")
        self.main.player.timer.grid_remove()
        self.main.player.tkraise()
        self.btn.config(text="Cancel",command=self.cancel)
        self.abort = False
        # Wait for player to hit button or user to cancel
        while not(self.abort):
            self.main.update()
            self.main.update_idletasks()
            num = self.game.buzz()
            if len(num) > 0:
                self.game.add(num[0],name)        
                self.game.H.append('+ '+name)
                self.game.A.play('d')
                break
        self.btn.config(text="Add",command=self.add)    
        self.new()
    def done(self):
        '''Returns back to main baord'''
        self.enter_change(0)
        if len(self.game.B)>0:
            self.main.board.tkraise()
            self.cont.board.tkraise()
        else:
            self.main.text.update('Setting Up Game')
            self.cont.start.tkraise()
    def remove(self,p):
        '''Removes player'''
        self.game.H.append('- '+self.game.P[p].name)
        del self.game.P[p]
        self.new()
    def cancel(self):
        '''Cancles adding a player'''
        self.abort = True
    def refresh(self):
        '''Refresh Button Devices'''
        self.game.reconnect()
            
class C_Advanced(tk.Frame):
    '''Allows user to access advanced features'''
    def __init__(self,cont,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        tk.Button(self,text="New Game",command=self.new_game,\
            bd=4,background='gray25',width=15,height=1).\
            grid(row=0,column=0,ipadx=10)
        tk.Button(self,text="Load Question",command=self.load_question,\
            bd=4,background='gray25',width=15,height=1).\
            grid(row=1,column=0,ipadx=10)
        tk.Button(self,text="Move to Board",command=self.load_board,\
            bd=4,background='gray25',width=15,height=1).\
            grid(row=2,column=0,ipadx=10)
        tk.Button(self,text="History",command=self.history,\
            bd=4,background='gray25',width=15,height=1).\
            grid(row=3,column=0,ipadx=10)
        tk.Button(self,text="Done",command=self.done,\
            bd=4,background='gray25',height=1).\
            grid(row=4,column=0,ipadx=10,ipady=0,pady=15,)
        self.grid_rowconfigure([0,1,2,3],weight=1,uniform='r')
        self.grid_columnconfigure(0,weight=1)
        self.grid(row=0,column=0,sticky="nsew")
    def new_game(self):
        '''Loads new game frame'''
        # Reminds user to save history
        self.game.save()
#        if len(self.game.H) > 0:
#            temp = Confirm(self.cont,self.main,"History will be deleted","Save","Skip")
#            if temp.wait():
#                file = filedialog.asksaveasfilename(title = "History File",defaultextension='.txt')    
#                with open(file,'w') as f:
#                    for line in self.game.H:
#                        f.write('\n'+line)
#            temp.destroy()
#            self.cont.lift()            
        self.game.P = {}
        self.game.H = []
        self.main.text.update('Setting Up New Game')
        self.cont.file.file.config(text="No File Selected")
        self.cont.file.folder.config(text="No Folder Selected")
        self.main.scores.label.config(text='')
        self.cont.file.tkraise()
    def load_question(self):
        '''Load a question from anywhere'''
        self.main.text.update('Loading Question')
        self.cont.board_select.new(temp=True)
    def load_board(self):
        '''Move to a new board'''
        # Board will start anew
        self.main.text.update('Moving Board')
        self.cont.board_select.new()
    def connect(self):
        '''Refresh buttons'''
        self.game.reconnect()
    def history(self):
        '''Open History'''
        History(self.cont,self.game)
    def done(self):
        '''Return to mainboard'''
        self.main.board.tkraise()
        self.cont.board.tkraise()

class History(tk.Toplevel):
    '''Allows user to see history in a pop out'''
    def __init__(self,cont,game):
        '''Creates Frame'''
        tk.Toplevel.__init__(self,cont)
        self.title("History")
        self.lift()
        text = tk.Text(self,font=('Consolas',14))
        text.insert("insert",'--------- Scores ---------\n')
        for p in game.ordered():
            name = game.P[p].name
            points = game.P[p].points
            text.insert("insert",'{:15s} {}\n'.format(name,points))
        text.insert("insert",'---------- Log -----------\n')
        for L in game.H:
            text.insert("insert",L+'\n')
        text.pack()
                
class C_Board_Select(tk.Frame):
    '''Allows user to select a new baord'''
    def __init__(self,cont,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        tk.Label(self,text='Select Board').grid(row=0,column=0)       
        self.S1 = tk.Frame(self)
        self.S1.grid(row=1,column=0)      
        tk.Button(self,text="Cancel",command=self.cancel,bd=4,background='gray25').\
            grid(row=2,column=0)
        self.grid_rowconfigure([0,1,2],weight=1)
        self.grid_columnconfigure(0,weight=1)  
        self.grid(row=0,column=0,sticky="nsew")
    def new(self,temp=False):
        '''Loads new window of baords'''
        self.S1.destroy()
        self.S1 = tk.Frame(self)
        for b in range(len(self.game.B)):
            tk.Button(self.S1,text=self.game.B[b].name,command=partial(self.go,b,temp),\
                bd=4,background='gray25').pack(pady=10)
        self.S1.grid(row=1,column=0) 
        self.tkraise()
    def go(self,b,temp):
        '''Moves to a board'''
        if not(temp):
            self.cont.board.new(b)
        else:
            self.cont.quest_select.new(b)
    def cancel(self):
        '''Returns to advanced menu'''
        self.cont.advanced.tkraise()
        self.main.text.update('Accessing Special Features')
        
class C_Quest_Select(tk.Frame):
    '''Allows user to select a question to load'''
    def __init__(self,cont,main,game):
        '''Create Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        self.S1 = tk.Frame(self)
        self.S1.grid(row=0,column=0,sticky="nsew")
        self.grid(row=0,column=0,sticky="nsew")
    def new(self,b):
        '''Load Board with questions to select'''
        self.S1.destroy()
        self.S1 = tk.Frame(self)
        c = 0
        for C in self.game.B[b].C:
            tk.Button(self.S1,text=C.name,anchor="center",wrap=200,relief='solid')\
                .grid(row=0,column=c,sticky="nsew")
            self.S1.grid_columnconfigure(c,weight=1,uniform='c')
            q = 0
            for Q in C.Q:
                self.S1.grid_rowconfigure(q+1,weight=1)
                tk.Button(self.S1,text=str(Q.points),command=partial(self.question,b,c,q),\
                    relief='solid').grid(row=q+1,column=c,sticky="nsew")
                q += 1
            c += 1   
        self.S1.grid(row=0,column=0,columnspan=3,sticky="nsew")
        self.tkraise()        
    def question(self,b,c,q):
        '''Selected a question'''
        self.cont.question.run(b,c,q,temp=True)
 
class C_Category(tk.Frame):
    '''Display Category Description'''
    def __init__(self,cont,main,game):
        '''Create Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        self.category = tk.Label(self)
        self.category.grid(row=0,column=0)
        self.description = tk.Label(self)
        self.description.grid(row=1,column=0)
        tk.Button(self,text="Done",command=self.done,bd=4,background='gray25').\
            grid(row=2,column=0,ipadx=10,ipady=0,padx=20,pady=15)
        self.grid_rowconfigure([0,1,2],weight=1)
        self.grid_columnconfigure(0,weight=1)    
        self.grid(row=0,column=0,sticky="nsew")
    def done(self):
        '''Return to Board'''
        self.main.board.tkraise()
        self.cont.board.tkraise()   
    def new(self,b,c):
        '''Load new category'''
        screen = self.main.category
        screen.category.config(text=self.game.B[b].C[c].name)
        screen.description.config(text=self.game.B[b].C[c].descript)
        screen.tkraise()
        width=self.winfo_width()
        self.category.config(text=self.game.B[b].C[c].name,wrap=width)
        self.description.config(text=self.game.B[b].C[c].descript,wrap=width)
        self.tkraise()
           
class C_Settings(tk.Frame):
    '''Allow user to adjust settings'''
    def __init__(self,cont,main,game):
        '''Create Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        tk.Label(self,text="Question Timer:",justify='left').\
            grid(row=1,column=0,sticky="w",pady=0)
        self.timer_question = tk.Entry(self,bg='gray35',width=5,justify='center')
        self.timer_question.grid(row=1,column=1,sticky="w",pady=0)
        tk.Label(self,text="Response Timer:",justify='left').\
            grid(row=2,column=0,sticky="w",pady=0)
        self.timer_response = tk.Entry(self,bg='gray35',width=5,justify='center')
        self.timer_response.grid(row=2,column=1,sticky="w",pady=0)
        tk.Label(self,text="Ans. Disp. Timer:",justify='left').\
            grid(row=3,column=0,sticky="w",pady=0)
        self.timer_answer = tk.Entry(self,bg='gray35',width=5,justify='center')
        self.timer_answer.grid(row=3,column=1,sticky="w",pady=0)
        self.multi_guess = tk.IntVar()
        tk.Label(self,text="Multi-Guess:",justify='left').\
            grid(row=1,column=3,sticky="w",pady=0)
        tk.Checkbutton(self,variable=self.multi_guess,fg='gray15').\
            grid(row=1,column=4,sticky="w",pady=0)    
        self.timer_bar = tk.IntVar()
        tk.Label(self,text="Timer Bar:",justify='left').\
            grid(row=2,column=3,sticky="w",pady=0)
        tk.Checkbutton(self,variable=self.timer_bar,fg='gray15').\
            grid(row=2,column=4,sticky="w",pady=0)      
        self.timer_txt = tk.IntVar()
        tk.Label(self,text="Timer Text:",justify='left').\
            grid(row=3,column=3,sticky="w",pady=0)
        tk.Checkbutton(self,variable=self.timer_txt,fg='gray15').\
            grid(row=3,column=4,sticky="w",pady=0)
        tk.Label(self,text="Sound Effect Volume:",justify='left').\
            grid(row=4,column=0,sticky="w",pady=0)
        self.alarm_vol = tk.Scale(self,from_=0,to=100,\
            length=200,orient='horizontal')
        self.alarm_vol.grid(row=4,column=1,sticky="w",pady=0)
        tk.Label(self,text="Question Volume:",justify='left').\
            grid(row=5,column=0,sticky="w",pady=0)
        self.music_vol = tk.Scale(self,from_=0,to=100,\
            length=200,orient='horizontal')
        self.music_vol.grid(row=5,column=1,sticky="w",pady=0)   
        tk.Button(self,text="Colors",command=self.colors,bd=4,background='gray25').\
            grid(row=5,column=3)
        tk.Button(self,text="Done",command=self.done,bd=4,background='gray25').\
            grid(row=6,column=1,columnspan=2,ipadx=10,ipady=0,padx=20,pady=15)
        self.grid_rowconfigure([1,2,3,4,5,6],weight=1)
        self.grid_columnconfigure([0,1,3,4],weight=1)    
        self.grid(row=0,column=0,sticky="nsew")
        self.load()
    def colors(self):
        self.cont.colors.tkraise()
    def done(self):
        '''Finish adjusting settings and save changes'''
        game = self.game
        game.S.timer_question = eval(self.timer_question.get())
        game.S.timer_response = eval(self.timer_response.get())
        game.S.timer_answer = eval(self.timer_answer.get())
        game.S.multi_guess = self.multi_guess.get()
        game.S.timer_bar = self.timer_bar.get()
        game.S.timer_txt = self.timer_txt.get()
        game.S.alarm_vol = self.alarm_vol.get()
        game.S.music_vol = self.music_vol.get()
        if game.S.timer_bar == 1:
            self.main.player.timer.bar.grid()
            self.main.question.timer.bar.grid()
        else:
            self.main.player.timer.bar.grid_remove()
            self.main.question.timer.bar.grid_remove()
        if game.S.timer_txt == 1:
            self.main.player.timer.txt.grid()
            self.main.question.timer.txt.grid()
        else:
            self.main.player.timer.txt.grid_remove()
            self.main.question.timer.txt.grid_remove()
        self.save()
        self.main.board.tkraise()
        self.cont.board.tkraise()   
    def reset(self):
        self.game.reset_settings()
        self.save()
    def load(self):
        try:
            with open("./files/misc/settings.pkl","rb") as file:
                self.game.S = pickle.load(file)
        except: self.reset()
        game = self.game
        self.timer_question.insert(0,str(game.S.timer_question))
        self.timer_response.insert(0,str(game.S.timer_response))
        self.timer_answer.insert(0,str(game.S.timer_answer))
        self.multi_guess.set(game.S.multi_guess)
        self.timer_bar.set(game.S.timer_bar)
        self.alarm_vol.set(game.S.alarm_vol)
        self.music_vol.set(game.S.music_vol) 
    def save(self):
        with open("./files/misc/settings.pkl","wb") as file:
            pickle.dump(self.game.S, file)

class C_Colors(tk.Frame):
    '''Allow user to adjust settings'''
    def __init__(self,cont,main,game):
        '''Create Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        tk.Label(self,text="Note: Color Change Requires Restart",justify='center').\
            grid(row=0,column=0,columnspan=2,pady=0)
        tk.Label(self,text="Background Color:",justify='left').grid(row=1,column=0,pady=0)
        self.bg = tk.Button(self,bd=4,command=self.get_bg,bg=game.S.color_bg,width=10)
        self.bg.grid(row=1,column=1,sticky='w')
        tk.Label(self,text="Title Bg Color:",justify='left').grid(row=2,column=0,pady=0)
        self.bg_dark = tk.Button(self,bd=4,command=self.get_bg_dark,bg=game.S.color_bg_dark,width=10)
        self.bg_dark.grid(row=2,column=1,sticky='w')
        tk.Label(self,text="Point Bg Color:",justify='left').grid(row=3,column=0,pady=0)
        self.bg_light = tk.Button(self,bd=4,command=self.get_bg_light,bg=game.S.color_bg_light,width=10)
        self.bg_light.grid(row=3,column=1,sticky='w')
        tk.Label(self,text="Text Color:",justify='left').grid(row=4,column=0,pady=0)
        self.txt = tk.Button(self,bd=4,command=self.get_txt,bg=game.S.color_txt,width=10)
        self.txt.grid(row=4,column=1,sticky='w')
        tk.Label(self,text="Timer Color:",justify='left').grid(row=5,column=0,pady=0)
        self.timer = tk.Button(self,bd=4,command=self.get_timer,bg=game.S.color_timer,width=10)
        self.timer.grid(row=5,column=1,sticky='w')
        tk.Button(self,text="Done",command=self.done,bd=4,background='gray25').\
            grid(row=6,column=0,columnspan=2,ipadx=10,ipady=0,padx=20,pady=15)
        self.grid_rowconfigure([0,1,2,3,4,5,6],weight=1)
        self.grid_columnconfigure([0,1],weight=1)
        self.grid(row=0,column=0,sticky="nsew") 
    def get_bg(self):
        color = askcolor()[1]
        self.game.S.color_bg = color
        self.bg.config(bg = color)
        self.tkraise();self.cont.lift()
    def get_bg_dark(self):
        color = askcolor()[1]
        self.game.S.color_bg_dark = color
        self.bg_dark.config(bg = color)
        self.tkraise();self.cont.lift()
    def get_bg_light(self):
        color = askcolor()[1]
        self.game.S.color_bg_light = color
        self.bg_light.config(bg = color)
        self.tkraise();self.cont.lift()
    def get_txt(self):
        color = askcolor()[1]
        self.game.S.color_txt = color
        self.txt.config(bg = color)
        self.tkraise();self.cont.lift()
    def get_timer(self):
        color = askcolor()[1]
        self.game.S.color_timer = color
        self.timer.config(bg = color)
        self.tkraise();self.cont.lift() 
    def done(self):
        with open("./files/Misc/settings.pkl","wb") as file:
            pickle.dump(self.game.S, file)
        self.cont.settings.tkraise()
   
        
class C_File(tk.Frame):
    '''File select for new game'''
    def __init__(self,cont,main,game):
        '''Create Frame'''
        tk.Frame.__init__(self,cont.frame)
        self.cont = cont
        self.main = main
        self.game = game
        tk.Button(self,text="Select Question File",command=self.select_file,\
            bd=4,background='gray25',width=23).grid(row=1,column=0,sticky='w',padx=20,pady=10)
        self.file = tk.Label(self,text="No File Selected")
        self.file.grid(row=1,column=1,padx=20,pady=10,sticky="w")
        tk.Button(self,text="Select Media Folder",command=self.select_folder,\
            bd=4,background='gray25',width=23).grid(row=2,column=0,sticky='w',padx=20,pady=10)
        self.folder = tk.Label(self,text="No Folder Selected")
        self.folder.grid(row=2,column=1,padx=20,pady=10,sticky="w")
        tk.Button(self,text="Done",command=self.done,\
            bd=4,background='gray25').grid(row=3,column=0,columnspan=2,ipadx=10,ipady=0,padx=20,pady=10)
        self.grid_rowconfigure([0,1,2,3],weight=1)
        self.grid_columnconfigure([0,1],weight=1)
        self.grid(row=0,column=0,sticky="nsew")        
    def select_file(self):
        '''Select question data file'''
        file = filedialog.askopenfilename(title = "Select Question File",filetypes = [("Supported File Types","*.xlsx;*.csv")])
        self.cont.lift()
        if file:
            self.game.new(file)
            self.file.config(text=file.split('/')[-1])
    def select_folder(self):
        '''Select image and music folder'''
        folder = filedialog.askdirectory(title = "Select Image Folder")
        self.cont.lift()
        if folder:
            self.game.F.folder = folder
            self.folder.config(text=folder.split('/')[-1])    
    def done(self):
        '''Finish selections'''
        # Check for missing files
        missing_files = self.game.check_files()
        if len(missing_files) > 0:
            temp = tk.Toplevel(self.cont)
            temp.title("Missing Files")
            temp.lift()
            text = tk.Text(temp)
            text.insert("insert",'_____Missing Files_____\n')
            for file in missing_files: text.insert("insert",file+'\n')
            text.pack()   
        else:
            if len(self.game.B) > 0:
                self.cont.board.new(0)
            else:
                self.cont.start.tkraise()
                self.main.text.update('Setting Up Game')

class Confirm(tk.Toplevel):
    '''Confirmation window with message'''
    def __init__(self,cont,main,text,yes,no):
        tk.Toplevel.__init__(self,cont)
        self.title("Confirmation")
        self.lift()
        self.main = main
        tk.Label(self,text = text).\
            grid(row=0,column=0,columnspan=2,sticky='nesw',padx=20,pady=10)
        tk.Button(self,text=yes,command=self.confirm,bd=4,background='gray25',width=5,height=1).\
            grid(row=1,column=0,sticky='nesw',padx=20,pady=10)
        tk.Button(self,text=no,command=self.cancel,bd=4,background='gray25',width=5,height=1).\
            grid(row=1,column=1,sticky='nesw',padx=20,pady=10)
        self.grid_columnconfigure([0,1],weight=1)
        self.grid_rowconfigure([0,1],weight=1)
        self.state = 0
    def wait(self):
        '''Wait for user input'''
        while self.state == 0:
            self.main.update()
            self.main.update_idletasks()
        if self.state == 1:
            return True
        else:
            return False
    def confirm(self):
        '''User confirm'''
        self.state = 1
    def cancel(self):
        '''User cancel'''
        self.state = -1
    
        
class How2Play(tk.Toplevel):
    '''Display information on how to play'''
    def __init__(self,cont):
        '''Create window'''
        tk.Toplevel.__init__(self,cont)
        self.title("How to Play")
        self.lift()
        text = tk.Text(self)
        with open('files\help.txt','r') as myfile:
            help_text = myfile.read()
        text.insert("insert",help_text)
        text.pack()    
 
'''Runs Program if File is clicked'''
if __name__ == "__main__":
    from TriviaProgram import MainWindow       
    main = MainWindow()
    main.mainloop()
                   
