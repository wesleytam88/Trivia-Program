'''Triva Program Code Package (1/4)'''

'''Code for display screen of Triva Program, refered to as main or screen in code
Display code is spars. Most functionality is located in the controller class'''

from Controller import Controller
from Game import Game
import tkinter as tk
from PIL import Image, ImageTk

class MainWindow(tk.Tk):
    '''Main window and handles tkinter backbone'''   
    def __init__(self):
        '''Creates initial window in which future frames will be loaded into'''
        tk.Tk.__init__(self)
        # Load app defaults
        self.iconbitmap(r"./files/misc/icon.ico")
        self.title("Game Board")
        self.geometry("350x160")
        self.option_add("*Font", "Calibri 14")
        self.tk_setPalette(background='gray15', foreground='gray99',\
               activeBackground='gray20', activeForeground='gray75')
        # Create frame for display screen
        self.frame = tk.Frame(self)
        self.frame.pack(side="top",fill="both",expand=True)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_columnconfigure(0,weight=1)
        # Initial Game
        self.game = Game()
        # Load Screen Selection board
        self.select = B_Select(self,self.game)
        self.select.tkraise()
        
        
class B_Select(tk.Frame):
    '''Allows user to select display screen'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame)
        self.main = main
        self.game = game
        tk.Label(self,wrap=320,text=\
            "Drag this window over the main screen for the audience, then press Select."\
            ).grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
        tk.Button(self,text="Select",command=self.selected,bd=4,background='gray25').\
            grid(row=1,column=0,ipadx=10,ipady=0,padx=20,pady=10)
        self.grid_rowconfigure([0,1],weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid(row=0,column=0,sticky="new")
    def selected(self):
        '''Creates all remaining frames and load start screen'''
        main = self.main
        main.frame.config(bg=self.game.S.color_bg)
        main.overrideredirect(True)
        main.state('zoomed')
        main.width = main.winfo_width()
        main.height = main.winfo_height()
        main.scale = (main.width/1536+main.height/864)/2
#        main.splash = B_Splash(main,main.game)
        main.board = B_Board(main,main.game)
        main.question = B_Question(main,main.game)
        main.answered = B_Answered(main,main.game)
        main.player = B_Player(main,main.game)
        main.scores = B_Scores(main,main.game)
        main.category = B_Category(main,main.game)
        main.text = B_Text(main,main.game)
        main.test= B_Test(main,main.game)
        main.text.update('Setting Up Game')
        cont = Controller(main,main.game)
        self.main.protocol("WM_DELETE_WINDOW", lambda:cont.on_closing(self.main,self.game))
        
class B_Board(tk.Frame):
    '''Main screeen that displayes questions'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame,bg=game.S.color_bg_dark)
        self.game = game
        self.main = main
        self.S1 = tk.Frame(self)
        self.S1.pack()
        self.grid(row=0,column=0,sticky="nsew")
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.pad = int(3*main.scale)
        
class B_Question(tk.Frame):
    '''Question Screen'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame,bg=game.S.color_bg)
        F = ("Arial",int(40*main.scale),"bold")  
        self.category = tk.Label(self,text="",\
           font=F,fg=game.S.color_txt,bg=game.S.color_bg_dark,wraplength=main.width*.9)
        self.category.grid(row=0,column=0,sticky='new',ipady=main.height*.03)
        self.question = tk.Label(self,text="",anchor='n',\
           font=F,fg=game.S.color_txt,bg=game.S.color_bg,wraplength=main.width*.9)
        self.question.grid(row=1,column=0,sticky="nsew") 
        self.pic = ImageTk.PhotoImage(Image.open("./files/misc/icon.ico"))
        self.image = tk.Label(self,image=self.pic,bg=game.S.color_bg)
        self.image.grid(row=2,column=0,sticky="nsew") 
        self.timer = B_Timer(self,main,game)
        self.timer.grid(row=3,column=0,sticky='sew')
        self.grid_rowconfigure([0,1,2,3],weight=1)
        self.grid_columnconfigure(0,weight=1)    
        self.grid(row=0,column=0,sticky="nsew")        
        
class B_Timer(tk.Frame):
    '''Timer Object
    Used in other frames to have an updatable timer bar and/or timer number'''
    def __init__(self,frame,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,frame,bg=game.S.color_bg)
        self.width = main.width
        self.height = main.height/20
        F = ("Arial",int(40*main.scale),"bold")
        self.txt = tk.Label(self,font=F,fg=game.S.color_txt,bg=game.S.color_bg)
        self.txt.grid(row=0,column=0)
        self.txt.grid_remove()
        self.bar = tk.Canvas(self,width=self.width,height=self.height,bg=game.S.color_bg,highlightthickness=0)
        self.tim = self.bar.create_rectangle(0,0,0,0,fill=game.S.color_timer,width=0)
        self.bar.grid(row=1,column=0,sticky='we')
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure([0,1],weight=1)
    def update(self,rem_time,del_time):
        '''Updates current timer value'''
        self.txt.config(text="{:.0f}".format(rem_time))
        if del_time < 1000:
            x0 = int(self.width/2*rem_time/del_time)
            y0 = 0
            x1 = int(self.width-self.width/2*rem_time/del_time)
            y1 = self.height
            self.bar.coords(self.tim,x0,y0,x1,y1)
        else:
            self.bar.coords(self.tim,0,0,0,0)
        
class B_Answered(tk.Frame):
    '''Screen showing answer after question has finished'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame,bg=game.S.color_bg)
        self.game = game
        self.main = main
        F = ("Arial",int(50*main.scale),"bold")
        self.answer = tk.Label(self,text="",\
            font=F,fg=game.S.color_txt,bg=game.S.color_bg,wraplength=main.width*.9)
        self.answer.grid(row=0,column=0)
        self.S1 = tk.Frame(self)
        self.S1.grid(row=1,column=0)
        self.grid_rowconfigure(0,weight=2)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid(row=0,column=0,sticky="nsew")
    def new(self,answer):
        '''Replaces text with new answer and updated player scores'''
        self.answer.config(text=answer)
        self.S1.destroy()
        self.S1 = tk.Frame(self,bg=self.game.S.color_bg)
        size = (self.main.height - self.answer.winfo_height())*.75*.6
        size = int(size/(1+len(self.game.P)))
        size = min([size,int(30*self.main.scale)])
        F = ("Arial",size,"bold")
        for r,p in enumerate(self.game.ordered()):
            tk.Label(self.S1,text=self.game.P[p].name,font=F,fg=self.game.S.color_txt,bg=self.game.S.color_bg).\
                grid(row=r,column=0,sticky="nesw",padx=size*.2)
            tk.Label(self.S1,text=self.game.P[p].points,font=F,fg=self.game.S.color_txt,bg=self.game.S.color_bg).\
                grid(row=r,column=1,sticky="nesw",padx=size*.2)
        self.S1.grid(row=1,column=0)
        self.tkraise()
        
class B_Player(tk.Frame):
    '''Displayes a combination of player name, message, and timer'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame,bg=game.S.color_bg)
        F = ("Arial",int(50*main.scale),"bold")        
        self.name = tk.Label(self,text="",font=F,fg=game.S.color_txt,bg=game.S.color_bg)
        self.name.grid(row=0,column=0,sticky="nsew")
        self.label = tk.Label(self,text="",\
            font=F,fg=game.S.color_txt,bg=game.S.color_bg,wraplength=main.width*.9)
        self.label.grid(row=1,column=0,sticky="nsew")
        self.timer = B_Timer(self,main,game)
        self.timer.grid(row=2,column=0,sticky='sew')
        self.grid_rowconfigure([0,1,2],weight=1)
        self.grid_columnconfigure(0,weight=1) 
        self.grid(row=0,column=0,sticky="nsew")
        
class B_Scores(tk.Frame):
    '''Display a list of players and scores'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame,bg=game.S.color_bg)
        self.game = game
        self.main = main
        F = ("Arial",int(40*main.scale),"bold")
        self.label = tk.Label(self,text="",font=F,fg=game.S.color_txt,bg=game.S.color_bg)
        self.label.pack(pady=self.main.scale*30)
        self.S1 = tk.Frame(self,bg=game.S.color_bg)
        self.S1.pack()
        self.grid(row=0,column=0,sticky="nsew")
    def new(self):
        '''Updates players and scores'''
        self.S1.destroy()
        self.S1 = tk.Frame(self,bg=self.game.S.color_bg)
        size = (self.main.height - self.label.winfo_height())*.75*.6
        size = int(size/(1+len(self.game.P)))
        size = min([size,int(30*self.main.scale)])
        F = ("Arial",size,"bold")
        for r,p in enumerate(self.game.ordered()):
            tk.Label(self.S1,text=self.game.P[p].name,\
               font=F,fg=self.game.S.color_txt,bg=self.game.S.color_bg).\
               grid(row=r,column=0,sticky="nesw",padx=size*.2)
            tk.Label(self.S1,text=self.game.P[p].points,\
               font=F,fg=self.game.S.color_txt,bg=self.game.S.color_bg).\
               grid(row=r,column=1,sticky="nesw",padx=size*.2)
            r += 1
        self.S1.pack()
        self.tkraise()
        
class B_Category(tk.Frame):
    '''Displayes category and description'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame,bg=game.S.color_bg)
        F = ("Arial",int(40*main.scale),"bold") 
        self.category = tk.Label(self,\
           font=F,fg=game.S.color_txt,bg=game.S.color_bg_dark,wraplength=main.width*.9)
        self.category.grid(row=0,column=0,sticky='new',ipady=main.height*.03)
        self.description = tk.Label(self,anchor='n',\
            font=F,fg=game.S.color_txt,bg=game.S.color_bg,wraplength=main.width*.9)
        self.description.grid(row=1,column=0,sticky='nsew')
        self.grid_rowconfigure([0,1],weight=1)
        self.grid_columnconfigure(0,weight=1)   
        self.grid(row=0,column=0,sticky="nsew")
        
class B_Test(tk.Frame):
    '''Test frame to allow for custom text wraping used in program
    Never displayed'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame)
        self.main = main
        self.text = tk.Label(self,text="Hello World")
        self.text.pack()
        self.grid(row=0,column=0,sticky="nsew")
    def font(self,txt,fnt,max_W,max_H):
        '''Returns max size for text wrapping into a certain area'''
        pnts = 1
        W = 0
        H = 0
        while W<=max_W and H<=max_H:
            pnts += 1
            self.wrap(txt,fnt,pnts,max_W)
            W = self.text.winfo_width()
            H = self.text.winfo_height()
        return [self.wrap(txt,fnt,pnts-1,max_W), pnts-1]
    def wrap(self,txt,fnt,pnts,max_W):
        '''Returns text wrapped to a certain width'''
        split_txt = txt.split()
        wrap_txt = split_txt[0]
        for wrd in split_txt[1:]:
            self.text.config(text=wrap_txt+' '+wrd,font=(fnt,pnts))
            self.main.update()
            if self.text.winfo_width()<max_W:
                wrap_txt += ' '+wrd
            else:
                wrap_txt += '\n'+wrd
        self.text.config(text=wrap_txt,font=(fnt,pnts))
        self.main.update()
        return wrap_txt

class B_Text(tk.Frame):
    '''Displayes a message'''
    def __init__(self,main,game):
        '''Creates Frame'''
        tk.Frame.__init__(self,main.frame,bg=game.S.color_bg)
        F = ("Arial",int(50*main.scale),"bold")        
        self.text = tk.Label(self,wraplength=main.width*.8,font=F,fg=game.S.color_txt,bg=game.S.color_bg)
        self.text.grid(row=0,column=0,sticky="nsew")
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1) 
        self.grid(row=0,column=0,sticky="nsew")
    def update(self,text):
        '''Changes text and loads screen'''
        self.text.config(text=text)
        self.tkraise()
                
'''Runs Program if File is clicked'''
if __name__ == "__main__":       
    main = MainWindow()
    main.mainloop()

    
