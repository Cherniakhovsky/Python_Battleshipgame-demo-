import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import Menu
from tkinter import Canvas
from tkinter import Spinbox
from tkinter import messagebox as mBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from numpy import arange, sin, pi
import matplotlib.ticker as mticker
from random import randint
import random
from itertools import cycle,repeat,takewhile


class Battleship():
    def __init__(self):
        self.win = tk.Tk()
        self.win.minsize(width=800, height=500)
        self.win.resizable(width=False, height=False)
        self.win.title("МОРСКОЙ БОЙ")
        self.win.iconbitmap('ship.ico')
        self.createWidgets()
        

        self._newgame()


        
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()
        
    def _newgame(self):
        self.freeDotsList=self.freeDots(10)
        #print (self.freeDotsList)

        self.matrix1=np.zeros(shape=(10,10))
        self.matrix2=np.zeros(shape=(10,10))
        
      
        #координаты (x,y) области вокруг кораблей, значение 1
        self.blockedTerritory = []
        #координаты (x,y) всех выстрелов, значение 2
        self.shotedTerritory = []
        #координаты (x,y) расположения кораблей, значение 5
        self.shipsLocation = []
        #координаты (x,y) всех клеток
        
        
        
        #repeat(self.createShip(1),10)

        try:
            self.createShip(2)
            self.createShip(2)
            self.createShip(2)
            self.createShip(1)
            self.createShip(1)
            self.createShip(1)
            self.createShip(1)

            
        except: print ("Слишком много кораблей!")
    

        self.locateShipOnMatrix(self.matrix1)

        self.drawMatrix(self.window1,self.matrix1,0,5)
        self.drawMatrix(self.window2,self.matrix2,7,0)
        #print ('self.blockedTerritory',self.blockedTerritory)
        #print ('self.shipsLocation',self.shipsLocation)
        
    def _msgBox(self):
        mBox.showinfo('Информация', 'Игра Морской бой.\nАвтор Черняховский Юрий.')

    def clickMe(self):
        self.shotData(self.matrix2)

        self.drawMatrix(self.window2, self.shotData(self.matrix2),7,0)
        
   
        
        
    def createWidgets(self):
        # Menu Control introduced here -----------------------
        menuBar = Menu(self.win) # 1
        self.win.config(menu=menuBar)
        fileMenu = Menu(menuBar) # 2
        fileMenu.add_command(label="Новая игра", command=self._newgame)
        fileMenu.add_separator() 
        fileMenu.add_command(label="Выход", command=self._quit)
        menuBar.add_cascade(label="Файл", menu=fileMenu)
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Информация", command=self._msgBox)
        menuBar.add_cascade(label="Помощь", menu=helpMenu)
        
        # Tab Control introduced here -----------------------
        tabControl = ttk.Notebook(self.win) # Create Tab Control
        tab1 = ttk.Frame(tabControl) # Create a tab
        tabControl.add(tab1, text='Поле 1') # Add the tab
        tab2 = ttk.Frame(tabControl) # Create second tab
        tabControl.add(tab2, text='Поле 2') # Add second tab
        tabControl.pack(expand=1, fill="both") # Pack make visible
        
        # Window Label
        self.window1 = ttk.LabelFrame(tab1, text=' МОЙ ФЛОТ ')
        self.window1.grid(column=0, row=0, padx=20, pady=10)
        
        # Window Label
        self.window2 = ttk.LabelFrame(tab1, text=' ФЛОТ ПРОТИВНИКА ')
        self.window2.grid(column=7, row=0, padx=20, pady=10)
        
        
        # Window with Buttons
        self.window3 = ttk.LabelFrame(tab1, text=' ВЫСТРЕЛ ')
        self.window3.grid(column=0, row=9,padx=20, pady=10, sticky='WE')
        
#        ttk.Label(self.monty2, text='ось X (А-К):').grid(column=0, row=0)
#        ttk.Label(self.monty2, text='ось Y (0-1):').grid(column=1, row=0)
        
        
        self.number = tk.StringVar() 
        self.numberChosen = ttk.Combobox(self.window3, width=7, textvariable=self.number, state='readonly')
        self.numberChosen['values'] = (['А','Б','В','Г','Д','Е','Ж','З','И','К']) 
        self.numberChosen.grid(column=0, row=1, padx=10, pady=10, sticky='W') 
        self.numberChosen.current(0)
        
        self.spin = Spinbox(self.window3, values=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9), width=7, bd=6)#,command=self._spin)
        self.spin.grid(column=1, row=1, pady=10)
        
        self.action=ttk.Button(self.window3, width=7, text="Запуск!",command=self.clickMe)
        self.action.grid(column=5, row=1, padx=10, pady=10) 
        


    #Функция выстрела по вражеским кораблям
    def shotData(self, matrix):
        x=self.spin.get()
        y=self.numberChosen.get()
        if y=='А': y=0
        elif y=='Б': y=1
        elif y=='В': y=2
        elif y=='Г': y=3
        elif y=='Д': y=4
        elif y=='Е': y=5
        elif y=='Ж': y=6
        elif y=='З': y=7
        elif y=='И': y=8
        elif y=='К': y=9
        else: print ('something wrong with y in shotData')
        
        matrix[x,y]=1
        print (matrix)
        return matrix
    
        
    #Рисуем матрицу и визуализируем в канвасе    
    def drawMatrix(self, window, matrix, x, y):        
        
             

        f = plt.Figure(figsize=(5, 5), dpi=65)
     
        labels = ['А','Б','В','Г','Д','Е','Ж','З','И','К']
        y_len=np.arange(len(labels))
    
        a = f.add_subplot(111)
        a.set_yticks(y_len)
        a.set_xticks(y_len)
        a.set_xticklabels(labels)
        a.imshow(matrix)


        canvas = FigureCanvasTkAgg(f, master=window)
        canvas.show()
        canvas.get_tk_widget().grid(column=x, row=y)
        canvas._tkcanvas.grid(column=x, row=y)

    
    def randomDot(self):

            body=(random.choice(self.freeDotsList))
            return body
            
            
    
    def locateShipOnMatrix(self,m):
        for blocked in self.blockedTerritory:
            m[blocked]=2
        
        for ship in self.shipsLocation:
            #print(ship)
            #print(m)
            m[ship]=5

        return m
    
    def freeDots(self,size):
        l=[]
        for i in range(size):
            for j in range(size):
                l.append((i,j))
        return l
    
    def createShip(self,deck):

        #position = random.choice (['vertical','horizontal'])
        dot=self.randomDot()
        #print ('dot =',dot)
            
        
        if deck==1:
            self.freeDotsListEmpting(dot)
            return dot
        
        elif deck==2:
            x1=dot[0]-1,dot[1]
            x2=dot[0]+1,dot[1]
            x3=dot[0],dot[1]-1
            x4=dot[0],dot[1]+1
            choice=random.choice([x1,x2,x3,x4])
            while choice in self.freeDotsList:
                newDot=choice
                break
    
            #print ('self.freeDotsList =',self.freeDotsList)
                
            self.freeDotsListEmpting(dot)
            self.freeDotsListEmpting(newDot)
            return dot, newDot



            
        elif deck==3: pass 
        elif deck==4: pass


            
        
        else: print('Введите правильное к-во палуб корабля. От 1 до 4')
        
     
        
    def freeDotsListEmpting(self,dot):
        #dot=self.randomDot()
        #while dot not in self.shipsLocation and dot not in self.blockedTerritory:
        self.shipsLocation.append(dot)

        try:self.freeDotsList.remove(dot)
        except:pass
        #print ('Self.randomDot() =',dot, dot)
        list=[]
        x=(dot[0]-1,dot[1]-1)
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        x=(dot[0]-1,dot[1])
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        x=(dot[0]-1,dot[1]+1)
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        x=(dot[0],dot[1]-1)
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        x=(dot[0],dot[1]+1)
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        x=(dot[0]+1,dot[1]-1)
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        x=(dot[0]+1,dot[1])
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        x=(dot[0]+1,dot[1]+1)
        list.append(x)
        if x not in self.shipsLocation:
            try: self.freeDotsList.remove(x) 
            except: pass
        
        #print(list)
        for i,j in list:
            if i>=0 and j>=0 and i<=9 and j<=9:
                if (i,j) not in self.shipsLocation:
                    self.blockedTerritory.append((i,j))

        return self.freeDotsList
        
     

   
if __name__=='__main__':

    print (Battleship().win.mainloop())        
        
        
        
        
