import tkinter as tk
import tkinter.font as tkFont
import uuid
<<<<<<< ours
<<<<<<< ours
<<<<<<< ours

class App:
    def __init__(self, root):
        # setting title
        self.root.title(str(uuid.uuid4())[:8])
        # setting window size
        width = 500
        height = 250
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.fontFamilly = "Calibri"

        title_label = tk.Label(root)
        ft = tkFont.Font(family=self.fontFamilly, size=22)
        title_label["font"] = ft
        title_label["fg"] = "#333333"
        title_label["justify"] = "center"
        title_label["text"] = "FortBot - Log in"
        title_label.place(x=140, y=10, width=219, height=69)

        email_label = tk.Label(root)
        ft = tkFont.Font(family=self.fontFamilly, size=12)
        email_label["font"] = ft
        email_label["fg"] = "#333333"
        email_label["justify"] = "center"
        email_label["text"] = "Email"
        email_label.place(x=50, y=100, width=70, height=25)

        email_entry = tk.Entry(root)
        email_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family=self.fontFamilly, size=10)
        email_entry["font"] = ft
        email_entry["fg"] = "#333333"
        email_entry["justify"] = "center"
        email_entry["text"] = ""
        email_entry.place(x=130, y=90, width=267, height=42)

        rembr_chkbx = tk.Checkbutton(root)
        ft = tkFont.Font(family=self.fontFamilly, size=10)
        rembr_chkbx["font"] = ft
        rembr_chkbx["fg"] = "#333333"
        rembr_chkbx["justify"] = "center"
        rembr_chkbx["text"] = "Remember me"
        rembr_chkbx.place(x=180, y=140, width=167, height=30)
        rembr_chkbx["offvalue"] = "0"
        rembr_chkbx["onvalue"] = "1"
        rembr_chkbx["command"] = self.rembr_chkbx_command

        login_btn = tk.Button(root)
        login_btn["bg"] = "#7915c6"
        ft = tkFont.Font(family=self.fontFamilly, size=10)
        login_btn["font"] = ft
        login_btn["fg"] = "#999999"
        login_btn["justify"] = "center"
        login_btn["text"] = "Login"
        login_btn.place(x=70, y=180, width=161, height=41)
        login_btn["command"] = self.login_btn_command

        free_tr_btn = tk.Button(root)
        free_tr_btn["bg"] = "#fad400"
        ft = tkFont.Font(family=self.fontFamilly, size=10)
        free_tr_btn["font"] = ft
        free_tr_btn["fg"] = "#000000"
        free_tr_btn["justify"] = "center"
        free_tr_btn["text"] = "Free Trial"
        free_tr_btn.place(x=280, y=180, width=161, height=41)
        free_tr_btn["command"] = self.free_tr_btn_command

    def rembr_chkbx_command(self):
        print("command")

    def login_btn_command(self):
        print("command")

    def free_tr_btn_command(self):
        print("command")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
=======
=======
>>>>>>> theirs
=======
>>>>>>> theirs
import os
import sys


def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)


class App:
    def __init__(self):
        self.root = tk.Tk()
        # setting title
        self.root.title(str(uuid.uuid4())[:8])
        self.root.iconbitmap(resource_path("bot_icon.ico"))
        # setting window size
        width = 500
        height = 250
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        self.fontFamily = "Calibri"

        self.title_label = tk.Label(self.root)
        ft = tkFont.Font(family=self.fontFamily, size=24)
        self.title_label["font"] = ft
        self.title_label["fg"] = "#333333"
        self.title_label["justify"] = "center"
        self.title_label["text"] = "FortBot - Log in"
        self.title_label.place(x=140, y=10, width=219, height=69)

        self.email_label = tk.Label(self.root)
        ft = tkFont.Font(family=self.fontFamily, size=14)
        self.email_label["font"] = ft
        self.email_label["fg"] = "#333333"
        self.email_label["justify"] = "center"
        self.email_label["text"] = "Email"
        self.email_label.place(x=50, y=100, width=70, height=25)

        self.email_entry = tk.Entry(self.root)
        self.email_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family=self.fontFamily, size=14)
        self.email_entry["font"] = ft
        self.email_entry["fg"] = "#333333"
        self.email_entry["justify"] = "left"
        self.email_entry["text"] = ""
        self.email_entry.place(x=130, y=90, width=267, height=42)

        self.rembr_chkbx = tk.Checkbutton(self.root)
        ft = tkFont.Font(family=self.fontFamily, size=12)
        self.rembr_chkbx["font"] = ft
        self.rembr_chkbx["fg"] = "#333333"
        self.rembr_chkbx["justify"] = "center"
        self.rembr_chkbx["text"] = "Remember me"
        self.rembr_chkbx.place(x=180, y=140, width=167, height=30)
        self.rembr_chkbx_value = tk.BooleanVar()
        self.rembr_chkbx["variable"] = self.rembr_chkbx_value
        # self.rembr_chkbx["variable"].set(False)
        self.rembr_chkbx["offvalue"] = 0
        self.rembr_chkbx["onvalue"] = 1
        self.rembr_chkbx["command"] = self.rembr_chkbx_command

        self.login_btn = tk.Button(self.root)
        self.login_btn["bg"] = "#6b42f4"
        ft = tkFont.Font(family="Franklin Gothic Medium", size=14, weight="bold")
        self.login_btn["font"] = ft
        self.login_btn["fg"] = "#ffffff"
        self.login_btn["justify"] = "center"
        self.login_btn["text"] = "Login"
        self.login_btn.place(x=70, y=180, width=161, height=41)
        self.login_btn["command"] = self.login_btn_command

        self.free_tr_btn = tk.Button(self.root)
        self.free_tr_btn["bg"] = "#fffa65"
        ft = tkFont.Font(family="Franklin Gothic Medium", size=14, weight="bold")
        self.free_tr_btn["font"] = ft
        self.free_tr_btn["fg"] = "#000000"
        self.free_tr_btn["justify"] = "center"
        self.free_tr_btn["text"] = "Free Trial"
        self.free_tr_btn.place(x=280, y=180, width=161, height=41)
        self.free_tr_btn["command"] = self.free_tr_btn_command
        self.root.mainloop()

    def rembr_chkbx_command(self):
        if self.rembr_chkbx_value.get():
            print("checked")
        else:
            print("unchecked")

    def login_btn_command(self):
        print(self.email_entry.get())

    def free_tr_btn_command(self):
        print(self.email_entry.get())


if __name__ == "__main__":
    app = App()
<<<<<<< ours
<<<<<<< ours
>>>>>>> theirs
=======
>>>>>>> theirs
=======
>>>>>>> theirs

