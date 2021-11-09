import pika, os, threading, json, datetime
from tkinter import *
from tkinter import font
from tkinter import ttk
import tkinter as tk
from pika.compat import time_now

exchange = 'sisdis'

url = os.environ.get('CLOUDAMQP_URL', 'amqps://tqzvyxix:oGh4wcsnvBrG2U5zzQBDgkcFH_ff8B8C@jackal.rmq.cloudamqp.com/tqzvyxix')
params = pika.URLParameters(url)

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
       
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
         
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False,
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        # create a Label
        self.pls = Label(self.login,
                       text = "Please login to continue",
                       justify = CENTER,
                       font = "Helvetica 14 bold")
         
        self.pls.place(relheight = 0.15,
                       relx = 0.2,
                       rely = 0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")
         
        self.labelName.place(relheight = 0.2,
                             relx = 0.1,
                             rely = 0.2)
         
        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                             font = "Helvetica 14")
         
        self.entryName.place(relwidth = 0.4,
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.2)
         
        # set the focus of the cursor
        self.entryName.focus()
         
        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text = "CONTINUE",
                         font = "Helvetica 14 bold",
                         command = lambda: self.goAhead(self.entryName.get()))
         
        self.go.place(relx = 0.4,
                      rely = 0.55)

        self.Window.mainloop()
 
    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
 
    def changeContext(self):
        self.isGroup = self.var1.get()

    # The main layout of the chat
    def layout(self,name):
       
        self.name = name
        self.var1 = tk.IntVar()
        self.isGroup = 0
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 1000,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A",
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
         
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
         
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
         
        self.textCons = Text(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14",
                             padx = 5,
                             pady = 5)
         
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)

        self.checkLabel = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
         
        self.checkLabel.place(relwidth = 1,
                               rely = 0.825)
         
        self.checkButton = Checkbutton(self.checkLabel, text='Group', variable=self.var1, onvalue=1, offvalue=0, command=self.changeContext)
        
        self.checkButton.place(relwidth = 0.2,
                               relheight = 0.05,
                               relx = 0.5,
                               rely = 0.008)

        self.entryRecipient = Entry(self.checkLabel,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
         
        # place the given widget
        # into the gui window
        self.entryRecipient.place(relwidth = 0.5,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)

        self.buttonJoin = Button(self.checkLabel,
                                text = "Join",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.initialize(self.entryRecipient.get()))
         
        self.buttonJoin.place(relx = 0.70,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)

        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
         
        self.labelBottom.place(relwidth = 1,
                               rely = 0.9)
        
         
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
         
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
         
        self.entryMsg.focus()
         
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
         
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06,
                             relwidth = 0.22)
         
        self.textCons.config(cursor = "arrow")
         
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
         
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
         
        scrollbar.config(command = self.textCons.yview)
         
        self.textCons.config(state = DISABLED)
 
    def initialize(self,queue):
        print('Joining...')

        self.queue = queue

        connectionPublisher = pika.BlockingConnection(params)
        self.channelPublisher = connectionPublisher.channel() # start a channe
        self.channelPublisher.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.channelPublisher.queue_declare(queue=self.name) # Declare a queue

        connectionConsumer = pika.BlockingConnection(params)
        self.channelConsumer = connectionConsumer.channel() # start a channel
        self.channelConsumer.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.channelConsumer.queue_declare(queue=self.name) # Declare a queue
        self.channelConsumer.queue_bind(queue=self.name, exchange=exchange)
        self.channelConsumer.basic_consume(self.name, self.message, auto_ack=True)

        self.consumerThread = threading.Thread(target=self.consumerConsume)
        self.consumerThread.start()

        self.textCons.config(state = NORMAL)
        self.textCons.insert(END, "Joining chat with " + (exchange if self.isGroup == 1 else queue) + "\n\n")
        self.textCons.config(state = DISABLED)
        self.textCons.see(END)

    def consumerConsume(self):
        self.channelConsumer.start_consuming()

    def message(self, channel, method, properties, body):
        print(f'\nMessage received: {body.decode()}')

        responseJson = json.loads(body)

        print(responseJson)

        self.textCons.config(state = NORMAL)
        self.textCons.insert(END, responseJson['timestamp'] + " " + responseJson['user'] + ": " + responseJson['message'] + "\n\n")
        self.textCons.config(state = DISABLED)
        self.textCons.see(END)
        

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg=msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target = self.publisher)
        snd.start()

    def publisher(self):
        try:
            self.timeNow = str(datetime.datetime.now().replace(microsecond=0).isoformat())

            jsonMessage = {}
            jsonMessage["user"] = self.name
            jsonMessage["timestamp"] = self.timeNow
            jsonMessage["message"] = self.msg
            jsonMessage["source"] = "group" if self.isGroup == 1 else "user"

            if self.isGroup == 0:
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, jsonMessage['timestamp'] + " " + jsonMessage['user'] + ": " + jsonMessage['message'] + "\n\n")
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

            self.channelPublisher.basic_publish(exchange=exchange if self.isGroup == 1 else '', routing_key='' if self.isGroup == 1 else self.queue, body=json.dumps(jsonMessage))
        except Exception as err:
            print("Ending the program...", err)
 
# create a GUI class object
g = GUI()