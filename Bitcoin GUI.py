import sys
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

import sqlite3 as lite
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

import time
import datetime
from datetime import timedelta
from exchanges.coindesk import CoinDesk

import threading
from threading import Thread

#Fonts
small_font = ("Sparkles",15)
medium_font = ("Sparkles",20)
large_font = ("Sparkles", 30)
normal_font = ("Bebas Neue",20)
small_norm = ("Bebas Neue",15)

class mainPage(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"Bitcoin Investment Simulator")
        self.attributes("-fullscreen",True)
        self.focus_force()
        container = tk.Frame(self)
        container.pack(side="top", fill="both",expand = True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        
        self.frames = {}
        
        for i in (mainMenu, Login, Register, Dashboard, Trade,HelpPage): #tuple of frames
        
            frame = i(container,self)
            self.frames[i] = frame
            frame.grid(row=0,column = 0, sticky = "nsew")       
        self.show_frame(mainMenu)

    def show_frame(self,point):
        frame = self.frames[point]
        frame.tkraise()

       
class mainMenu(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent,bg="#0088FF")
        label = tk.Label(self,text = "Bitcoin Trading Simulator",anchor = "center",font=large_font,bg="#0088FF")
        label.pack()
        label.place(relx=0.5,rely=0.1,anchor="center")

        login = ttk.Button(self,text = "Login",command = lambda: controller.show_frame(Login))
        login.pack()
        login.place(relx=0.5,rely=0.3, relwidth = 0.2,relheight = 0.1,anchor = "center")

        register = ttk.Button(self,text = "Register",command = lambda: controller.show_frame(Register))
        register.pack()
        register.place(relx=0.5,rely=0.5, relwidth = 0.2, relheight = 0.1, anchor = "center")

        Quit = ttk.Button(self, text = "Exit", command=quit)
        Quit.pack()
        Quit.place(relx=0.5,rely=0.7, relwidth = 0.2,relheight = 0.1, anchor = "center")

rowID = ""
valid = "Not Logged"
logged = False

def LogVal(self,userEnt,passEnt,controller):
    global rowID
    global valid
    global logged

    User = userEnt.get()
    Pass = passEnt.get()

    #select where username and passowrd is in the same record

    con = lite.connect("bitcoin.db")
    cur = con.cursor()
    cur.execute("SELECT rowid FROM credentials WHERE (username)=(?)",(User,))
    data = cur.fetchone()
    con.commit

    print ("ROW ID IS",data)
    
    cur.execute("SELECT rowid FROM credentials WHERE (password)=(?)",(Pass,))
    data2 = cur.fetchone()
    con.commit()

    #data and data2 are both the rowid of the user 
    
    print ("ROW ID IS",data2)

    if data == None or data2 == None:
        noneLabel=tk.Label(self, text = "Incorrect username or password",bg="#ACE6FF")
        noneLabel.pack()
        noneLabel.place(relx=0.4405,rely=0.66)
      
    elif data == data2:
        print ("Login Successful")
        valid  = "Logged"
        userEnt.delete(0,"end")
        passEnt.delete(0,"end")
        logged=True
        rowID = data2
        controller.show_frame(Dashboard)            
    else:
        elseLabel=tk.Label(self, text = "Incorrect username or password",bg="#ACE6FF")
        elseLabel.pack()
        elseLabel.place(relx=0.4405,rely=0.66)

class Login(tk.Frame):
    
    def __init__(self, parent,controller):
        
        tk.Frame.__init__(self, parent,bg="#0088FF")
  
        label = tk.Label(self,text = "Login",anchor = "center",font=large_font,bg="#0088FF")
        label.pack()
        label.place(relx=0.5,rely=0.10,anchor="center")

        #username
        uLabel=tk.Label(self, text = "Username",bg="#ACE6FF",font = small_norm)
        uLabel.pack()
        uLabel.place(relx=0.4305,rely=0.358)
                
        userEnt = ttk.Entry(self)
        userEnt.pack()
        userEnt.place(relx=0.5,rely=0.4, relwidth = 0.14,relheight = 0.03,anchor = "center")
        
        #password
        pLabel=tk.Label(self, text = "Password",bg="#ACE6FF",font=small_norm)
        pLabel.pack()
        pLabel.place(relx=0.4305,rely=0.458)
    
        passEnt = ttk.Entry(self,show="*")
        passEnt.pack()
        passEnt.place(relx=0.5,rely=0.5, relwidth = 0.14,relheight = 0.03,anchor = "center")

        submit = ttk.Button(self, text = "Continue", command = lambda: LogVal(self,userEnt,passEnt,controller))
        submit.pack()
        submit.place(relx=0.5,rely=0.6, relwidth = 0.08,relheight = 0.03,anchor = "center")
        
        back = ttk.Button(self, text = "Back", command = lambda:clear_login(self,userEnt,passEnt,controller))
        back.pack()
        back.place(relx=0.05,rely=0.95, relwidth = 0.06,relheight = 0.05,anchor = "center")


#to clear fields when back is pressed on login page
def clear_login(self,userEnt,passEnt,controller):
    userEnt.delete(0,"end")
    passEnt.delete(0,"end")
    controller.show_frame(mainMenu)

def RegVal(self,user_ent,pass_ent,conf_pass,controller):
 
    con = lite.connect("bitcoin.db")    
    cur = con.cursor()
    data = cur.fetchone()

    user_grab = user_ent.get()
    pass_grab = pass_ent.get()
    conf_grab = conf_pass.get()
    
    #validation

    cur.execute("SELECT * FROM credentials WHERE username=?",(user_grab,))
    data = cur.fetchone()
    con.commit()

    cur.execute("SELECT * FROM credentials WHERE password=?",(pass_grab,))
    data2 = cur.fetchone()
    con.commit()

    print ("USERS ARE",data)
    if data != None:
        presentLabel=tk.Label(self, text = "Username taken",bg="#ACE6FF")
        presentLabel.pack()
        presentLabel.place(relx=0.6305,rely=0.56)

    elif data2 != None:
        passLabel=tk.Label(self, text = "Password taken",bg="#ACE6FF")
        passLabel.pack()
        passLabel.place(relx=0.7305,rely=0.56)        

    elif len(pass_grab) < 8:
        charLabel=tk.Label(self, text = "Password must be 8 characters",bg="#ACE6FF")
        charLabel.pack()
        charLabel.place(relx=0.6305,rely=0.361)
        
    elif pass_grab != conf_grab:
        matchLabel=tk.Label(self, text = "Passwords must match",bg="#ACE6FF")
        matchLabel.pack()
        matchLabel.place(relx=0.6305,rely=0.46)
        
    else:
        cur.execute("INSERT INTO credentials (username,password,usd_balance) VALUES (?,?,?)", (user_grab,pass_grab,10000))
        con.commit()
        controller.show_frame(Login) 
        print ("Registration successful")
    
                    
class Register(tk.Frame):    
    def __init__(self, parent,controller):
         
        tk.Frame.__init__(self, parent,bg="#0088FF")
  
        label = tk.Label(self,text = "Registration",anchor = "center",font=large_font,bg="#0088FF")
        label.pack()
        label.place(relx=0.5,rely=0.1,anchor="center")

        #username
        uLabel=tk.Label(self, text = "Selcect Username",bg="#ACE6FF",font=small_norm)
        uLabel.pack()
        uLabel.place(relx=0.4305,rely=0.358)
        
        user_ent = ttk.Entry(self)
        user_ent.pack()
        user_ent.place(relx=0.5,rely=0.4, relwidth = 0.14,relheight = 0.03,anchor = "center")      

        #password
        pLabel=tk.Label(self, text = "Enter Password",bg="#ACE6FF",font=small_norm)
        pLabel.pack()
        pLabel.place(relx=0.4305,rely=0.458)
    
        pass_ent = ttk.Entry(self,show="*")
        pass_ent.pack()
        pass_ent.place(relx=0.5,rely=0.5, relwidth = 0.14,relheight = 0.03,anchor = "center")

        #confirm password
        confLabel=tk.Label(self, text = "Confirm Password",bg="#ACE6FF",font=small_norm)
        confLabel.pack()
        confLabel.place(relx=0.4305,rely=0.558)
    
        conf_pass = ttk.Entry(self,show="*")
        conf_pass.pack()
        conf_pass.place(relx=0.5,rely=0.6, relwidth = 0.14,relheight = 0.03,anchor = "center")
        
        back = ttk.Button(self, text = "Back", command = lambda: clear_reg(self,user_ent,pass_ent,conf_pass,controller))
        back.pack()
        back.place(relx=0.05,rely=0.95, relwidth = 0.06,relheight = 0.05,anchor = "center")
        
        submit = ttk.Button(self, text = "Continue", command = lambda: RegVal(self,user_ent,pass_ent,conf_pass,controller))
        submit.pack()
        submit.place(relx=0.5,rely=0.7, relwidth = 0.08,relheight = 0.03,anchor = "center")


#to clear register fields when back is pressed
def clear_reg(self,user_ent,pass_ent,conf_pass,controller):
    user_ent.delete(0,"end")
    pass_ent.delete(0,"end")
    conf_pass.delete(0,"end")
    controller.show_frame(mainMenu)
    
def usdPass(self):
    global rowID

    con = lite.connect('bitcoin.db')
    cur = con.cursor()
    cur.execute("SELECT usd_balance FROM credentials WHERE rowid=?",(rowID))
    data = cur.fetchone()
    con.commit()
    #return data

    usd_label = tk.Label(self,name="usd_label",text = (data,"USD"), anchor = "center",font = small_font,bg="#0088FF")
    usd_label.place(relx=0.1,rely=0.18,anchor="center")

    print ("USD balance is",data)  

def btcPass(self):
    global rowID
    global back

    con = lite.connect('bitcoin.db')
    cur = con.cursor()
    cur.execute("SELECT btc_balance FROM credentials WHERE rowid=?",(rowID))
    data = cur.fetchone()
    con.commit()
    if data[0] == None:
        data = 0
    split = "."
    balance = str(data[0]).split(split,1)[0]+"."+str(data[0]).split(split,1)[1][:2] #to two decimal places
        
    #name parameter removes overlapping
    btc_label = tk.Label(self,name="btc_label",text = (balance,"BTC"),anchor = "center",font = small_font,bg="#0088FF")
    btc_label.place(relx=0.25,rely=0.18,anchor="center")
    
    return btc_label
  
#Dashboard window displaying wallet and purchase buttons. User balance is also displayed to the user. 
class Dashboard(tk.Frame):

    def __init__(self, parent,controller):
        global rowID
        global font

        tk.Frame.__init__(self, parent,bg="#0088FF")
    
        title = tk.Label(self,text = "DASHBOARD",anchor = "center",font=large_font,bg="#0088FF")
        title.pack()
        title.place(relx=0.5,rely=0.1,anchor="center")

#INFO TEXT BOX
        info_text = tk.Text(self,bg="#0088FF",height = 46,width=40)
        info_text.config(state="normal",font=normal_font)
        info_text.insert(tk.INSERT,"                                Welcome to the Bitcoin Trading Simulator\n\n")
        info_text.insert(tk.INSERT,"               Please read the Information before you begin trading")
        info_text.place(relx=0.5,rely=0.24,relwidth = 0.4,relheight = 0.12,anchor = "center")
        info_text.config(state="disabled")
        
        trade = tk.Button(self, text = "TRADE BITCOIN", command = lambda: controller.show_frame(Trade),relief=RIDGE,bg="#BFF1FF",font = ('Sparkles',15))
        trade.place(relx=0.27,rely=0.60,relwidth = 0.40,relheight = 0.46,anchor = "center")

        help_window = tk.Button(self, text = "Help & Information", command = lambda: controller.show_frame(HelpPage),relief=RIDGE,bg="#BFF1FF",font = ('Sparkles',15))
        help_window.place(relx=0.7,rely=0.60,relwidth = 0.40,relheight = 0.46,anchor = "center")
       
        show_usd = ttk.Button(self, text = "Show USD Balance", command = lambda: usdPass(self))
        show_usd.place(relx=0.1,rely=0.11, relwidth = 0.1,relheight = 0.05,anchor = "center")

        show_btc = ttk.Button(self, text = "Show BTC Balance", command = lambda: btcPass(self))
        show_btc.place(relx=0.25,rely=0.11, relwidth = 0.1,relheight = 0.05,anchor = "center")

        back = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(mainMenu))
        back.place(relx=0.05,rely=0.95, relwidth = 0.06,relheight = 0.05,anchor = "center")


currentVal = False
present = 0

live_showing = False
past_showing = False

live_fig = plt.figure(figsize = (5,5), dpi=100)
ax = live_fig.add_subplot(111)

live_fig.suptitle("Bitcoin Live Chart", fontsize = 14, fontweight = "bold",ha="center")
live_fig.text(0.5,0.08,"Time",fontsize = 14, fontweight = "bold",ha="center")
live_fig.text(0.03,0.57,"Price USD",fontsize = 14, fontweight = "bold",rotation = "vertical",va="center")

#possibly use wait_variable()

#Lablels for balance in 'Trade' Window 
def usd_balance(self):
    global rowID
    con = lite.connect('bitcoin.db')
    cur = con.cursor()
    cur.execute("SELECT usd_balance FROM credentials WHERE rowid=?",(rowID))
    data = cur.fetchone()
    con.commit()
    #name parameter removes overlapping
    usd_label = tk.Label(self,name="usd_label",text = (data,"USD"),anchor = "center",font=small_font, bg="#ACE6FF")
    usd_label.place(relx=0.675,rely=0.35,anchor="center")    
    print ("USD balance is",data)

def btc_balance(self):
    global rowID
    con = lite.connect('bitcoin.db')
    cur = con.cursor()
    cur.execute("SELECT btc_balance FROM credentials WHERE rowid=?",(rowID))
    data = cur.fetchone()
    real = str(data[0])[:6]
    print ("REAL",real)
    con.commit()
    #name parameter removes overlapping
    btc_label = tk.Label(self,name="btc_label",text = (real,"BTC"),anchor = "center",font=small_font, bg="#ACE6FF")
    btc_label.place(relx=0.88,rely=0.35,anchor="center")    
    print ("BTC balance is",data)

class Trade(tk.Frame):
    
    def __init__(self, parent,controller):
                    
        id_thread = threading.Thread(target = logged)
        id_thread.daemon = True
        id_thread.start()

        tk.Frame.__init__(self, parent,bg="#0088FF")
        global rowID
        global real_price
        title = tk.Label(self,text = "BTC/USD Trading Pair",anchor = "center",font=large_font,bg="#0088FF")
        title.pack()
        title.place(relx=0.5,rely=0.1,anchor="center")

#INFO FUNCTIONS        

        def update():
#LABLE SHOWING LIVE BITCOIN PRICE

            while True:
                current_price = CoinDesk().get_current_price(currency = 'USD')
                bitcoin_price = current_price[:-5].replace(",","")

                live_price = tk.Label(self,name="livePrice",text =("$",bitcoin_price),font=large_font,bg="#A2A2A2",fg="#0054FF")
                live_price.place(relx=0.615,rely=0.94,relwidth=0.1,anchor="center")
                print (bitcoin_price)
                time.sleep(5)            

        thread = threading.Thread(target = update)
        thread.start()

        def last_bought():
            global rowID

            con = lite.connect('bitcoin.db')
            cur = con.cursor()            
            cur.execute("SELECT last_bought FROM credentials WHERE rowid=?",(rowID))
            data = cur.fetchone()
            con.commit()
            last = str(data[0])

            bought_label = tk.Label(self,name="lastBought",text =("$",last),font=large_font,bg="#A2A2A2",fg="#0054FF")
            bought_label.place(relx=0.76,rely=0.94,anchor="center")

        def profit():
            global rowID

            con = lite.connect('bitcoin.db')
            cur = con.cursor()            
            cur.execute("SELECT last_bought FROM credentials WHERE rowid=?",(rowID))
            data = cur.fetchone()
            con.commit()
            last = str(data[0])
            
            current_price = CoinDesk().get_current_price(currency = 'USD')
            bitcoin_price = current_price[:-5].replace(",","")

            difference = int(bitcoin_price) - int(data[0])
            percent = (difference/int(data[0]))*100
            real_percent = str(percent)
            perc = real_percent[:5]

            profit_label = tk.Label(self,name="profit",text =(perc,"%"),font=large_font,bg="#A2A2A2",fg="#0054FF")
            profit_label.place(relx=0.905,rely=0.94,anchor="center")
            
#PANELS
        right_panel=tk.Label(self,bg="#ACE6FF")
        right_panel.pack()
        right_panel.place(relx=0.57,rely=0.20,relwidth = 0.415,relheight = 0.55)

        buy_panel=tk.Label(self,bg="#A2A2A2")
        buy_panel.pack()
        buy_panel.place(relx=0.5795,rely=0.45,relwidth = 0.197,relheight = 0.29)

        sell_panel=tk.Label(self,bg="#A2A2A2")
        sell_panel.pack()
        sell_panel.place(relx=0.783,rely=0.45,relwidth = 0.197,relheight = 0.29)

        lower_panel=tk.Label(self,bg="#ACE6FF")
        lower_panel.pack()
        lower_panel.place(relx=0.015,rely=0.8,relwidth = 0.97,relheight = 0.18)
        
        chart_panel=tk.Label(self,bg="#A2A2A2")
        chart_panel.pack()
        chart_panel.place(relx=0.021,rely=0.812,relwidth = 0.52,relheight = 0.105)

        hist_panel=tk.Label(self,bg="#A2A2A2")
        hist_panel.pack()
        hist_panel.place(relx=0.55,rely=0.81,relwidth = 0.43,relheight = 0.16)

        options_title = tk.Label(self,text = "Chart Options:",anchor = "center",font=small_font,bg="#A2A2A2")
        options_title.pack()
        options_title.place(relx=0.09,rely=0.84,anchor="center")

        usdBalance = ttk.Button(self,text = "USD Balance",command = lambda: usd_balance(self))
        usdBalance.place(relx=0.675,rely=0.3,relwidth = 0.15,relheight = 0.045,anchor="center")

        btcBalance = ttk.Button(self, text = "BTC Balance",command = lambda: btc_balance(self))
        btcBalance.place(relx=0.88,rely=0.3, relwidth = 0.15,relheight = 0.045,anchor = "center")

#BUYING        
        buy_title = tk.Label(self,text = "BUY",anchor = "center",font=large_font,bg="#A2A2A2")
        buy_title.pack()
        buy_title.place(relx=0.68,rely=0.5,anchor="center")
        
        buy_label = tk.Label(self,text = "Enter BTC amount",anchor = "center",bg="#0088FF")
        buy_label.pack()
        buy_label.place(relx=0.675,rely=0.59,relwidth = 0.13,relheight = 0.03,anchor="center")

        buy_ent = ttk.Entry(self)
        buy_ent.pack()
        buy_ent.place(relx=0.675,rely=0.62, relwidth = 0.13,relheight = 0.03,anchor = "center")

        buy_button = ttk.Button(self, text = "Purchase",command = lambda: purchase())
        buy_button.place(relx=0.675,rely=0.68, relwidth = 0.08,relheight = 0.03,anchor = "center")

#SELLING        
        sell_title = tk.Label(self,text = "SELL",anchor = "center",font=large_font,bg="#A2A2A2")
        sell_title.pack()
        sell_title.place(relx=0.88,rely=0.5,anchor="center")

        sell_label = tk.Label(self,text = "Enter BTC amount",anchor = "center",bg="#0088FF")
        sell_label.pack()
        sell_label.place(relx=0.88,rely=0.59,relwidth = 0.13,relheight = 0.03,anchor="center")

        sell_ent = ttk.Entry(self)
        sell_ent.pack()
        sell_ent.place(relx=0.88,rely=0.62, relwidth = 0.13,relheight = 0.03,anchor = "center")

        sell_button = ttk.Button(self, text = "Sell",command = lambda: sell())
        sell_button.place(relx=0.88,rely=0.68, relwidth = 0.08,relheight = 0.03,anchor = "center")

#CHART BUTTONS
        live_chart = ttk.Button(self, text = "Live Chart",command = lambda: my_thread())
        live_chart.place(relx=0.4965,rely=0.865, relwidth = 0.08,relheight = 0.09,anchor = "center")

        week = ttk.Button(self, text = "1 Week",command = lambda: week())
        week.place(relx=0.06,rely=0.89, relwidth = 0.06,relheight = 0.03,anchor = "center")

        month = ttk.Button(self, text = "1 Month",command = lambda: month())
        month.place(relx=0.13,rely=0.89, relwidth = 0.06,relheight = 0.03,anchor = "center")

        six_months = ttk.Button(self, text = "6 Months",command = lambda: sixmonths())
        six_months.place(relx=0.20,rely=0.89, relwidth = 0.06,relheight = 0.03,anchor = "center")
        
        year = ttk.Button(self, text = "1 Year",command = lambda: year())
        year.place(relx=0.27,rely=0.89, relwidth = 0.06,relheight = 0.03,anchor = "center")

        three_years = ttk.Button(self, text = "3 Years",command = lambda: three_years())
        three_years.place(relx=0.34,rely=0.89, relwidth = 0.06,relheight = 0.03,anchor = "center")

#TOOLS PANNEL

        tools_title = tk.Label(self,text = "Tools:",anchor = "center",font = normal_font,bg="#0054FF")
        tools_title.place(relx=0.5695 ,rely=0.831,anchor="center")
                    
        price_title = tk.Label(self,text = "Current Price",anchor = "center",font = small_font,bg="#A2A2A2")
        price_title.place(relx=0.62,rely=0.88,anchor="center")

        bought_title = tk.Button(self,text = "Last Bought",anchor = "center",relief=RIDGE,font = small_font,bg="#A2A2A2",command =lambda: last_bought())
        bought_title.place(relx=0.76,rely=0.88,anchor="center")

        profit_title = tk.Button(self,text = "Current Profit",anchor = "center",relief=RIDGE,font = small_font,bg="#A2A2A2",command =lambda: profit())
        profit_title.place(relx=0.905,rely=0.88,anchor="center")
        
        back = ttk.Button(self, text = "Back", command = lambda: back_trade(controller,sell_ent,buy_ent))
        back.place(relx=0.05,rely=0.95, relwidth = 0.06,relheight = 0.05,anchor = "center")

        Help = ttk.Button(self, text = "Help & Information", command = lambda: controller.show_frame(HelpPage))
        Help.place(relx=0.10,rely=0.1, relwidth = 0.14,relheight = 0.07,anchor = "center")

        def back_trade(controller,sell_ent,buy_ent):
            sell_ent.delete(0,"end")
            buy_ent.delete(0,"end")
            controller.show_frame(Dashboard)

        def clear_label(completed):
            completed.place_forget()

        def update_buy(buy_sum,new_usd,new_btc,real_price):
            global rowID
            con = lite.connect('bitcoin.db')
            cur = con.cursor()
            cur.execute("UPDATE credentials SET (usd_balance,btc_balance,last_bought) = (?,?,?) WHERE rowid = ? ",(int(new_usd),float(new_btc),int(real_price), int(rowID[0])))
            con.commit()

            completed = tk.Label(self,text = "Transaction Complete",bg="#A2A2A2",fg="#00FF4C")
            completed.place(relx=0.675,rely=0.72,anchor="center")

        def update_sell(sell_sum,new_usd,new_btc,real_price):
            global rowID
            con = lite.connect('bitcoin.db')
            cur = con.cursor()
            cur.execute("UPDATE credentials SET (usd_balance,btc_balance) = (?,?) WHERE rowid = ? ",(int(new_usd),float(new_btc), int(rowID[0])))            
            con.commit()

            completed = tk.Label(self,text = "Transaction Complete",bg="#A2A2A2",fg="#00FF4C")
            completed.place(relx=0.88,rely=0.72,anchor="center")

        def buy_popup(buy_sum,new_usd,new_btc,real_price):
            question = tkinter.messagebox.askquestion("Warning!",("Are you sure you wish to purchase",buy_sum," Bitcoin?\n        Transactions are non-refundable"))
            if question == "yes":
                update_buy(buy_sum,new_usd,new_btc,real_price)
                

        def sell_popup(sell_sum,new_usd,new_btc,real_price):
            question = tkinter.messagebox.askquestion("Warning!",("Are you sure you wish to sell",sell_sum,"Bitcoin?\nTransactions are non-refundable"))
            if question == "yes":
                update_sell(sell_sum,new_usd,new_btc,real_price)
            
            
        def purchase():
            global rowID
            buy_sum_string = buy_ent.get() #amount they wish to buy
            buy_sum=""            
            try:
                buy_sum = float(buy_sum_string) #convert to float
            except ValueError:
                numbers = tkinter.messagebox.showinfo("Warning!","Please use numbers only")

            if buy_sum_string == (""):
                print("Empty Field")
            elif isinstance(buy_sum,float):                                
                con = lite.connect('bitcoin.db')
                cur = con.cursor()
                cur.execute("SELECT btc_balance FROM credentials WHERE rowid=?",(rowID))
                btc_balance = cur.fetchone()
                con.commit()

                con = lite.connect('bitcoin.db')
                cur = con.cursor()
                cur.execute("SELECT usd_balance FROM credentials WHERE rowid=?",(rowID))
                usd_balance = cur.fetchone()
                
                if usd_balance[0] == None:
                    usd_balance = (0,)
                if btc_balance[0] == None:
                    btc_balance = (0,)

                print ("usd balance is",usd_balance) #usd_balance seen as a tuple, converted below
                print ("btc balance is",btc_balance)

                valid_usd = usd_balance[0]
                valid_btc = btc_balance[0]

                if usd_balance == 0:
                    broke_box = tkinter.messagebox.showinfo("Warning!","You do not have enough funds for this purchase")

                if usd_balance!=0:                
                    current_price = CoinDesk().get_current_price(currency = 'USD')
                    real_price = current_price[:-5].replace(",","")  #convert price to compatable format
                    real_desired = float(buy_sum)*float(real_price)  #convert desired BTC amount to USD using current price 
                    print ("Desired buy is",real_desired)
                                          
                    if float(real_desired) > float(usd_balance[0]):
                        broke_box = tkinter.messagebox.showinfo("Warning!","You do not have enough funds for this purchase")
                    else:
                        new_usd = valid_usd - real_desired
                        new_btc = valid_btc + float(buy_sum)
                        print ("New USD is",new_usd)
                        print ("New BTC is",new_btc)
                        buy_popup(buy_sum,new_usd,new_btc,real_price)
            else:
                print ("You must use numbers only")
   
        def sell():
            global rowID
            sell_sum=""    
            sell_sum_string = sell_ent.get() #amount they wish to sell
            try:
                sell_sum = float(sell_sum_string) #attempt to convert to float
            except ValueError:
                numbers = tkinter.messagebox.showinfo("Warning!","Please use numbers only") #if it cannot be covnerted then given value must not be a number

            print ("You want to sell", sell_sum,"BTC")

            if sell_sum_string == (""):
                print ("Empty Field")
                
            elif isinstance(sell_sum,float): 
            
                con = lite.connect('bitcoin.db')
                cur = con.cursor()
                cur.execute("SELECT btc_balance FROM credentials WHERE rowid=?",(rowID))
                btc_balance = cur.fetchone()
                con.commit()
                
                con = lite.connect('bitcoin.db')
                cur = con.cursor()
                cur.execute("SELECT usd_balance FROM credentials WHERE rowid=?",(rowID))
                usd_balance = cur.fetchone()
                
                if usd_balance[0] == None:
                    usd_balance = 0
                if btc_balance[0] == None:
                    btc_balance = 0

                print ("usd balance is",usd_balance) #usd_balance seen as a tuple, converted below
                print ("btc balance is",btc_balance)

                valid_usd = usd_balance[0]
                valid_btc = btc_balance[0]

                if btc_balance == 0:
                    broke_box = tkinter.messagebox.showinfo("Warning!","You do not have enough funds for this sale")

                elif btc_balance!=0:
                    current_price = CoinDesk().get_current_price(currency = 'USD')
                    real_price = current_price[:-5].replace(",","")  #convert price to compatable format
                    real_desired = float(sell_sum)*float(real_price)  #convert desired BTC amount to USD using current price 
                    print ("Desired sell is",real_desired)

                    if float(sell_sum) > float(btc_balance[0]):
                        broke_box = tkinter.messagebox.showinfo("Warning!","You do not have enough bitcoin to sell")
                    else:
                        new_usd = valid_usd + real_desired
                        new_btc = valid_btc - float(sell_sum) #as entry is seen as string,convert to float
                        print ("New USD is",new_usd)
                        print ("New BTC is",new_btc)
                        sell_popup(sell_sum,new_usd,new_btc,real_price)
            else:
                print ("Please use numbers only")


        def my_thread():            
            t = threading.Thread(target = getPrice)
            t.daemon = True  
            t.start()

            s = threading.Thread(target = func)
            s.daemon = True  
            s.start()
    
        def liveChart(i = None):
            global live_fig
            global live_showing

            live_showing = True

            if live_showing == True:

                counter = 0
                c = open("priceData.txt","r")
                currentData = c.read()
                c.close()
                lines = currentData.split("\n")
                #print (lines)

                x3 = []
                y3 = []
                for line in lines:
                    counter = counter+1
                    
                    if len(line)>1:
                        real_price = line.split(',',2)
                        x = real_price[1]
                        realx = x[:-7] #rounding down
                        y =real_price[0]
                        realy = y[:-5] #rounding down
                        #print ("LIVE")
                        y3.append(float(realy))
                        x3.append(counter)
                        
                plt.style.use("fivethirtyeight")
                live_fig.patch.set_facecolor("#0088FF")
                ax.clear()
                ax.plot(x3,y3,color = "#00FF4C")                
                ax.tick_params(labelsize=10)
                ax.set_facecolor("#3F3F3F")
                live_fig.autofmt_xdate()                            

        def getPrice():
            global present

            bitcoinPrice = []

            if present == 0: #global variable present to clear file only on first time run
                open("priceData.txt", "w").close() #clearing file before new price data is saved

            while True:
                currentTime = datetime.datetime.now()                    
                currentPrice = CoinDesk().get_current_price(currency = 'USD')
                currentPrice = currentPrice.replace(",", "") #removing comma from prices to obtain integer value
                bitcoinPrice.append(currentPrice)
                my_list = []
                x = datetime.datetime.now().time()
                my_list.append(x)
                #print (currentPrice, currentTime)
                time.sleep(5)                               
                #Current price is fetched and saved to text file every 5 seconds and then plotted on the chart
                
                with open("priceData.txt", "a") as priceData:
                    priceData.write(str(currentPrice)+","+str(my_list[0])+"\n")
                present +=1
            
        def func():            
            live_canvas = FigureCanvasTkAgg(live_fig, self)       
            ani = animation.FuncAnimation(live_fig, liveChart, interval = 1000)            
            live_canvas.draw()
            live_canvas.get_tk_widget().place(relx=0.3,rely=0.47, relwidth = 0.55,relheight = 0.55,anchor = "center")                    
            print ("ani working")

        def past_plot():
            global past_showing
            past_showing = True

            f = open("pastData.txt","r")            
            counter = 0            
            filecount = len(open("pastData.txt").readlines(  ))
            
            x2 = []
            y2 = []
            lines = f.readlines()
            #for line in f.readlines():
            step = 0
            
            if filecount <14:
                step=1
            elif filecount >=30 and filecount <63:
                step=7
            elif filecount >=180 and filecount <360:
                step=31
            elif filecount >=365 and filecount <1095:
                step = 93
            elif filecount >=1095:
                step = 365

            labels =[]

            for x in range(0,filecount,1):        
                graphData = lines[x].strip ("\n").split(",")
                                    
                if len(lines[x])>1:
                    y = float(graphData[1])
                    
                    x = datetime.datetime.strptime(graphData[0], '%Y-%m-%d').strftime('%d/%b/%Y')                
                    c = counter
                    x2.append(c)
                    y2.append(y)
                    
                    if counter%step==0:
                        labels.append(x)
                    else:
                        labels.append("")
                #after every line read, counter increases by 1 inside for loop
                counter += 1
            f.close()
            
            if past_showing == True:                
                past_fig = plt.figure(figsize = (5,5), dpi=100)
                
                plt.style.use('fivethirtyeight')
                #must define style before sublot
                a = past_fig.add_subplot(111)
                a.plot(x2,y2,color = "#00FF4C")
                
                plt.title("Bitcoin Past Chart", fontsize = 14, fontweight = "bold")
                plt.xlabel("Time", fontsize = 14, fontweight = "bold")
                plt.ylabel("Price (USD)", fontsize = 12, fontweight = "bold")
                
                past_canvas = FigureCanvasTkAgg(past_fig, self) #adding figure to canvas
                past_canvas.draw()
                past_canvas.get_tk_widget().place(relx=0.3,rely=0.47, relwidth = 0.55,relheight = 0.6,anchor = "center")

                #a.set_xticklabels(labels)
                a.tick_params(axis=u'both', which=u'both',length=0,labelsize=10)            
                past_fig.autofmt_xdate()
                
                a.set_facecolor("#3F3F3F")
                past_fig.patch.set_facecolor("#0088FF")

    #past week graph

        def week():
            end_date = datetime.datetime.now()
            real_end = end_date.strftime("%Y-%m-%d")
                            
            week_delta = datetime.timedelta(days=7)

            start_date = end_date - week_delta
            
            real_start = start_date.strftime("%Y-%m-%d")
            #may not need to round down for week
            pastPrice = CoinDesk().get_historical_data_as_dict(start=real_start, end=real_end)
            write_data(pastPrice)
                    
    #past month
        def month():
            end_date = datetime.datetime.now()
            
            real_end = end_date.strftime("%Y-%m-%d")
            
            month_delta = datetime.timedelta(days=31)

            start_date = end_date - month_delta
            real_start = start_date.strftime("%Y-%m-%d")
            #rounding down to the first of the month
            real_start=real_start[:len(real_start)-2]+"01"                
            
            pastPrice = CoinDesk().get_historical_data_as_dict(start=real_start, end=real_end)
            write_data(pastPrice)
    #past 6 months
        def sixmonths():
            end_date = datetime.datetime.now()
            real_end = end_date.strftime("%Y-%m-%d")
                            
            six_delta = datetime.timedelta(days=180)

            start_date = end_date - six_delta
            real_start = start_date.strftime("%Y-%m-%d")
            #rounding down to the first of the month
            real_start=real_start[:len(real_start)-2]+"01"
                            
            pastPrice = CoinDesk().get_historical_data_as_dict(start=real_start, end=real_end)
            write_data(pastPrice)

    #past 1 year
        def year():
            end_date = datetime.datetime.now()
            real_end = end_date.strftime("%Y-%m-%d")                
            
            year_delta = datetime.timedelta(days=365)

            start_date = end_date - year_delta
            real_start = start_date.strftime("%Y-%m-%d")
            #rounding down to the first of the month
            real_start=real_start[:len(real_start)-2]+"01"
                            
            pastPrice = CoinDesk().get_historical_data_as_dict(start=real_start, end=real_end)
            write_data(pastPrice)

    #past 3 years
        def three_years():
            end_date = datetime.datetime.now()
            real_end = end_date.strftime("%Y-%m-%d")
            
            triple_delta = datetime.timedelta(days=1095)

            start_date = end_date - triple_delta
            real_start = start_date.strftime("%Y-%m-%d")
            #rounding down to the first of the month
            real_start=real_start[:len(real_start)-2]+"01"
            
            pastPrice = CoinDesk().get_historical_data_as_dict(start=real_start, end=real_end)
            write_data(pastPrice)
    #Writing data to file             
        def write_data(pastPrice): #passing "pastPrice" through as paramater
            global past_showing
            open("pastData.txt", "w").close()
            with open("pastData.txt","a") as pastData:
                for i in pastPrice:
                    #i is first element, being the date
                    #i is also the index for the price in the dictionary
                    pastData.write(str(i)+","+str(pastPrice[i])+"\n")
            past_showing = True
            past_plot()
        week()



class HelpPage(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent,bg="#0088FF")

        title = tk.Label(self,text = "HELP & INFORMATION",anchor = "center",font=large_font,bg="#0088FF")
        title.pack()
        title.place(relx=0.5,rely=0.1,anchor="center")

        right_panel=tk.Label(self,bg="#ACE6FF")
        right_panel.pack()
        right_panel.place(relx=0.54,rely=0.20,relwidth = 0.415,relheight = 0.55)

        left_panel=tk.Label(self,bg="#ACE6FF")
        left_panel.pack()
        left_panel.place(relx=0.05,rely=0.20,relwidth = 0.415,relheight = 0.55)

#LEFT PANEL INFO
        livePrice = tk.Label(self,text = "Current Price:",anchor = "center",font=medium_font,bg="#ACE6FF")
        livePrice.pack()
        livePrice.place(relx=0.14,rely=0.25,anchor="center")

        price_info = tk.Text(self,bg="#DEDEDE",height = 46,width=40)
        price_info.config(state="normal",font=small_norm)
        price_info.insert(tk.INSERT," - This widget shows the current price of bitcoin\n\n")
        price_info.insert(tk.INSERT," - This is a real-time widget that updates every 5 seconds")
        price_info.place(relx=0.26,rely=0.33,relwidth = 0.4,relheight = 0.1,anchor = "center")
        price_info.config(state="disabled")

        Buttons = tk.Label(self,text = "Buttons:",anchor = "center",font=medium_font,bg="#ACE6FF")
        Buttons.pack()
        Buttons.place(relx=0.11,rely=0.51,anchor="center")

        button_text = tk.Text(self,bg="#DEDEDE",height = 46,width=40)
        button_text.config(state="normal",font=small_norm)
        button_text.insert(tk.INSERT,"The buttons within the program perform various tasks:\n\n")
        button_text.insert(tk.INSERT," - Within the Trade window, there are several buttons to change the time scale of the chart\n\n")
        button_text.insert(tk.INSERT," - Other buttons such as the USD and BTC balance will display your balance\n\n - Click these buttons to update your balance")
        button_text.place(relx=0.26,rely=0.64,relwidth = 0.4,relheight = 0.2,anchor = "center")
        button_text.config(state="disabled")
#RIGHT PANEL INFO

        lastbought = tk.Label(self,text = "Last Bought:",anchor = "center",font=medium_font,bg="#ACE6FF")
        lastbought.pack()
        lastbought.place(relx=0.62,rely=0.25,anchor="center")

        last_text = tk.Text(self,bg="#DEDEDE",height = 46,width=40)
        last_text.config(state="normal",font=small_norm)
        last_text.insert(tk.INSERT," -  This widget shows the price of Bitcoin last time you made a purchase\n\n")
        last_text.insert(tk.INSERT," - You can view this by clicking the 'Last Bought' button in the trade window\n\n")
        last_text.place(relx=0.75,rely=0.33,relwidth = 0.4,relheight = 0.1,anchor = "center")
        last_text.config(state="disabled")
        
        profit_title = tk.Label(self,text = "Current Profit:",anchor = "center",font=medium_font,bg="#ACE6FF")
        profit_title.pack()
        profit_title.place(relx=0.64,rely=0.51,anchor="center")

        currentProfit = tk.Text(self,bg="#DEDEDE",height = 46,width=40)
        currentProfit.config(state="normal",font=small_norm)
        currentProfit.insert(tk.INSERT," -  This widget shows the percentage change in the price of Bitcoin since you last bought\n\n")
        currentProfit.insert(tk.INSERT," -  You should use this as an indicator for future purchases\n\n")
        currentProfit.insert(tk.INSERT," - You can view this by clicking the 'Current Profit' button in the trade window\n\n")
        currentProfit.place(relx=0.75,rely=0.64,relwidth = 0.4,relheight = 0.2,anchor = "center")
        currentProfit.config(state="disabled")
#main buttons
        dash = ttk.Button(self, text = "Dashboard", command = lambda: controller.show_frame(Dashboard))
        dash.place(relx=0.4,rely=0.82, relwidth = 0.18,relheight = 0.08,anchor = "center")

        trade = ttk.Button(self, text = "Trade", command = lambda: controller.show_frame(Trade))
        trade.place(relx=0.6,rely=0.82, relwidth = 0.18,relheight = 0.08,anchor = "center")    

app = mainPage()
app.mainloop()






