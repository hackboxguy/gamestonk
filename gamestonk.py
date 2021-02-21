#!/usr/bin/env python3
import finnhub
import json
import random
import tkinter as tk
from tkinter.font import Font
import requests
import time
import re

myvars = {}
with open("/home/pi/gamestonk/settings.txt") as myfile:
    for line in myfile:
        name, var = line.split("=")
        myvars[name.strip()] = var

symbol = myvars["symbol"]
symbol = re.sub(r"[\n\t\s]*", "", symbol)
my_key=myvars["api_key"]
my_key = re.sub(r"[\n\t\s]*", "", my_key)
finnhub_client = finnhub.Client(api_key=my_key)

class Gui(tk.Tk):
    """
    Main GUI designed for 3.5inch display.
    """
    def __init__(self, *args, **kwargs):

        self.PADDING_X = 10
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("{0}x{1}+0+0".format(width, height))
        self.title("Quote of the Day")
        self.overrideredirect(1)

        self.quote = tk.StringVar()
        self.author = tk.StringVar()

        quote_frame = tk.Frame(bg="#dcdcda")
        quote_frame.pack(fill=tk.X)

        quote_args = {
            "bg": "#dcdcda",
            "wraplength": width - self.PADDING_X * 2,
            "justify": "left",
            "textvariable": self.quote,
        }
        quote_font = Font(family="Open Sans", size=50, slant="italic")
        quote_label = tk.Label(quote_frame, **quote_args)
        quote_label.configure(font=quote_font)
        quote_label.grid(padx=(self.PADDING_X, 0), pady=(100, 0))

        author_frame = tk.Frame(bg="#dcdcda")
        author_frame.pack(fill=tk.BOTH, expand=True)

        author_args = {
            "bg": "#dcdcda",
            "textvariable": self.author,
        }
        author_font = Font(family="Open Sans", size=32)
        author_label = tk.Label(author_frame, **author_args)
        author_label.configure(font=author_font)
        author_label.grid(padx=(self.PADDING_X, 0), pady=(50, 0))

        footer_frame = tk.Frame(bg="#dcdcda")
        footer_frame.pack(fill=tk.BOTH)

        quit_args = {
            "command": self.quit,
            "text": "Quit",
            "bg": "#ffffff",
            "borderwidth": 0,
        }
        quit_button = tk.Button(footer_frame, **quit_args)
        quit_button.pack(side=tk.RIGHT, padx=(2,15), pady=5)

        update_args = {
            "command": self.update,
            "text": "Update",
            "bg": "#ffffff",
            "borderwidth": 0
        }
        update_button = tk.Button(footer_frame, **update_args)
        update_button.pack(side=tk.RIGHT, pady=5)

        self.update()
        self.auto_update()

    def update(self):
        """ Update labels """
        try:
            request = self.request()
            qvalue = "GME:%s" % (request['c'])
            qvalue = qvalue[:9] #"GME:%s" % (request['c'])
            self.quote.set(qvalue) #request['c'])
        except:
            pass

    def request(self):
        """ Query TheySaidSo API """
        response = finnhub_client.quote(symbol)
        #print(response["c"])
        return response

    def auto_update(self):
        """ Auto update ticker """
        self.after(5000, self.auto_update) #refresh rate is 5sec
        self.update()

def main():
    """ Run main GUI """
    gui = Gui()
    gui.mainloop()

if __name__ == "__main__":
    main()
