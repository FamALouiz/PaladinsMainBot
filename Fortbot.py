import os
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import E, END, TRUE
import tkinter.font as tkFont
import requests, datetime, time, mainbotloop, uuid, sys, re
import pyautogui
from firebase_admin import db
import firebase_admin


def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)


class App:
    def __init__(self):
        self.root = tk.Tk()
        # setting title
        self.cred = firebase_admin.credentials.Certificate(
            {
                "type": "service_account",
                "project_id": "testing-python-9d5ff",
                "private_key_id": "d0dd0f69a26d73b1ef30812ef04146d02f146d07",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCoZlHUBMQSHfTM\njc2brxjGM10fu5UXYvBklBgJ3MJcQHxqFx9bO87I7nlZvwZMzI7PEVHWr5jT2oXd\nj6rxKlCpOuyD6pDxATkwmFsCgqpTxSIAjvQk0mp4X8GmFRrDqOg0kvkkGxS9TNBX\n/S+CVLP7fy9wXrBSLHyTlEeJ6TRFgy2iL8Qv7dv3VnIz/5/FFukCXCDKO5no2sQ9\njysN6ffB2oQXB0Bg2K7ir0FyQ3QJdRHfvlAjKPAMiQhDeNd0gzr95FGB8Z+fzIev\n3xSYgRwfA+up/c3TOPnLvRQ74LIGz3UHbxFw1UMyj1t973FHWHtoR0A7mQNVnKij\n1ImbMNE7AgMBAAECggEALGd2kkKDdQeDImEN40xjavfmSVTMNnN3Uf4e7JLSiULT\ny6G3OfZmS2NeikSto5iY248ElmiNEuffPpIAkEEJLeaEsTAr8fDRpLe338yWnyov\nEhif1gnJ213ckS+ldAxY1mwe199wM45KrbjsSyCMqPdbifTd530liECkMIBWsTE9\nLJLFh6PKS+P4TodWJOK5FPUhYS2s+mmkcQ+PoyMpkxY6Ihno9pJOt7rxYORn1ufl\n8cNAPiECZbzgmCLnXAxXjGZHi7wOA7e9eGobM9aBkvIL1439c0OdHFxwAJue9mxC\nprlfNWkOioemxIOpwCn27Ab4OmQ+zhs2DCbKy1iNgQKBgQDb3EIBxjAxSojQPdSO\nS3aGrtxjFaHDuzQP9a2hJh+ozRG7o79ctsQl0nzDmJcF2vEckScyunhRSjZhHbpU\n0M2xCaef6+5bQVyrDCCOuFapz9CG7hd2u2PJKk5R2aCu7tluIZPv6KOYR+m6LBEH\nLDPUbQ5bfeA03JnhWLtHWLVdwQKBgQDEFJd3csXM7fsQbAD0/9fJ7Mae7qu6xW0B\nijuRTVP+XVRP+nUhU+dGRD5itqvfFs1dFXMw4jhLG8Aq5w8XRMVZ8iLUT0gzO4Yr\nPX1geKKn2uq0XWs4qVWi4E9NzBnyUtQSf1fSMRG2858T9mp2MmAsaSiBaH19EJZH\nXpTWcREl+wKBgQCWm7Vjvb35phM+g3x91VfmPxadkY30pOKvJB7Cy3jYi1HgdfV6\nr4CCYEQzQO4Dhs2wQgbWC0KsfOfvcwvXWgntgq2fMWFghc/TJEWRPtmvDbrNE4Bj\nR0692Qs5qpkV/GxZswrCR1z5zhlf/RvVDASdOe+h4QKbc5q98aio4S2sgQKBgDnx\nt90Vrrxjq2jr8dB09qj2bq+y6k7UXuUwm2/SATtPC0ZjRk/mApdyPVlgkCPqEiAq\n4ZKVl3sipURIad4/dW6iLoa9MyHoujp2/mEO5UpjWC6a2L+y0trCHM1pvlUtAvzA\nYwx7cbe2ANGeZVGui1s0bELpxQO7bh2DJsrEOQQXAoGATekXJGKOIRz3jNm1Qvqd\nAf4OzYU7zpHTLPZEmSJ9ubbZa75nzwjPpE8sf8a6FPMRdgaYvg6aHbOaOW9OEStL\nEqqh4SQFXrh+s+vMzbaCNMEo5V870r6MnHRHOULSwtPvo7GNZz/u0/vBfw+SXq+o\nyyaIznMaaznadiBdGgfE03k=\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-fek1b@testing-python-9d5ff.iam.gserviceaccount.com",
                "client_id": "110568083276339576805",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fek1b%40testing-python-9d5ff.iam.gserviceaccount.com",
            }
        )
        self.firebase = firebase_admin.initialize_app(
            self.cred,
            {
                "databaseURL": "https://anubisproducts-53639.firebaseio.com/",
            },
        )
        self.root.title(str("AnubisCrystalBot"))
        self.root.iconbitmap("bot_icon.ico")
        # setting window size
        width = 500
        height = 400
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        self.fontFamily = "Calibri"
        self.mainbot = None
        self.tier = 3
        self.login = False

        self.title_label = tk.Label(self.root)
        ft = tkFont.Font(family=self.fontFamily, size=24)
        self.title_label["font"] = ft
        self.title_label["fg"] = "#333333"
        self.title_label["justify"] = "center"
        self.title_label["text"] = "AnubisCrystalBot - Log in"
        self.title_label.place(x=10, y=10, width=500, height=69)

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

        self.password_label = tk.Label(self.root)
        ft = tkFont.Font(family=self.fontFamily, size=14)
        self.password_label["font"] = ft
        self.password_label["fg"] = "#333333"
        self.password_label["justify"] = "center"
        self.password_label["text"] = "Password"
        self.password_label.place(x=50, y=160, width=80, height=25)

        self.password_entry = tk.Entry(self.root)
        self.password_entry["borderwidth"] = "1px"
        ft = tkFont.Font(family=self.fontFamily, size=14)
        self.password_entry["font"] = ft
        self.password_entry["fg"] = "#333333"
        self.password_entry["justify"] = "left"
        self.password_entry["text"] = ""
        self.password_entry.place(x=130, y=150, width=267, height=42)

        self.rembr_chkbx = tk.Checkbutton(self.root)
        ft = tkFont.Font(family=self.fontFamily, size=12)
        self.rembr_chkbx["font"] = ft
        self.rembr_chkbx["fg"] = "#333333"
        self.rembr_chkbx["justify"] = "center"
        self.rembr_chkbx["text"] = "Remember me"
        self.rembr_chkbx.place(x=180, y=300, width=167, height=30)
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
        self.login_btn.place(x=180, y=330, width=161, height=41)
        self.login_btn["command"] = self.login_btn_command

        self.root.mainloop()

    def showAttackScroll(self):
        text = tk.Text(self.root)
        text.grid(row=2, column=1)
        self.sbFlank = tk.Scrollbar(self.root, command=text.yview)
        self.sbFlank.grid(row=2, column=1)
        text.configure(yscrollcommand=self.sbFlank.set)
        for i in range(10):
            button = tk.Button(text)
            text.window_create("end", window=button)
            text.insert("end", "\n")
        text.configure(state="disabled")

    def showSupportScroll(self):
        text = tk.Text(self.root)
        text.place(x=1200, y=20, width=200, height=500)
        button = tk.Button(text="Groove", command=self.setSupportChampionGrover)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Corvus", command=self.setSupportChampionCorvus)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Furia", command=self.setSupportChampionFuria)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Grohk", command=self.setSupportChampionGrohk)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Io", command=self.setSupportChampionIo)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Jenos", command=self.setSupportChampionJenos)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Lillith", command=self.setSupportChampionLillith)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Maldamba", command=self.setSupportChampionMaldamba)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Pip", command=self.setSupportChampionPip)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Rei", command=self.setSupportChampionRei)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Seris", command=self.setSupportChampionSeris)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        button = tk.Button(text="Ying", command=self.setSupportChampionYing)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        text.configure(state="disabled")

    def setSupportChampionGrover(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "GROVER"
        self.print_to_GUI("Picking Grover")

    def setSupportChampionCorvus(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "CORVUS"
        self.print_to_GUI("Picking Corvus")

    def setSupportChampionFuria(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "FURIA"
        self.print_to_GUI("Picking Furia")

    def setSupportChampionGrohk(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "GROHK"
        self.print_to_GUI("Picking Grohk")

    def setSupportChampionGrover(self):
        print("GROVER")
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "GROVER"
        self.print_to_GUI("Picking Grover")

    def setSupportChampionIo(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "IO"
        self.print_to_GUI("Picking Io")

    def setSupportChampionJenos(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "JENOS"
        self.print_to_GUI("Picking Jenos")

    def setSupportChampionLillith(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "LILLITH"
        self.print_to_GUI("Picking Lillith")

    def setSupportChampionMaldamba(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "MAL'DAMBA"
        self.print_to_GUI("Picking Mal'Damba")

    def setSupportChampionPip(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "PIP"
        self.print_to_GUI("Picking Pip")

    def setSupportChampionRei(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "REI"
        self.print_to_GUI("Picking Rei")

    def setSupportChampionSeris(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "SERIS"
        self.print_to_GUI("Picking Seris")

    def setSupportChampionYing(self):
        mainbotloop.championType = "Support"
        mainbotloop.championSelected = True
        mainbotloop.champion = "YING"
        self.print_to_GUI("Picking Ying")

    def clickFlankChampion(self):
        print("TEST2")

    def clear(self):
        widget_list = self.root.place_slaves()
        for widget in widget_list:
            widget.place_forget()

    def rembr_chkbx_command(self):
        if self.rembr_chkbx_value.get():
            print("checked")
        else:
            print("unchecked")

    def free_tr_btn_command(self):
        self.tier = 0
        self.clear()
        width = 750
        height = 400
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        self.lastMessage = None
        self.fontFamily = "Calibri"

        self.startButton = tk.Button(self.root)
        self.startButton["bg"] = "#22ff00"
        ft = tkFont.Font(family=self.fontFamily, size=10)
        self.startButton["font"] = ft
        self.startButton["fg"] = "#000000"
        self.startButton["justify"] = "center"
        self.startButton["text"] = "Start"
        self.startButton["state"] = "normal"
        self.startButton.place(x=40, y=50, width=100, height=40)
        self.startButton["command"] = self.startBot

        self.stopButton = tk.Button(self.root)
        self.stopButton["bg"] = "#ff0000"
        ft = tkFont.Font(family=self.fontFamily, size=10)
        self.stopButton["font"] = ft
        self.stopButton["fg"] = "#000000"
        self.stopButton["justify"] = "center"
        self.stopButton["text"] = "Stop"
        self.stopButton["state"] = "disabled"
        self.stopButton.place(x=40, y=120, width=100, height=40)
        self.stopButton["command"] = self.stopBot

        self.textBox = tk.Text(self.root)
        self.textBox["borderwidth"] = "1px"
        ft = tkFont.Font(family=self.fontFamily, size=10)
        self.textBox["font"] = ft
        self.textBox["fg"] = "#333333"
        self.textBox.place(x=180, y=50, width=520, height=260)
        self.textBox.tag_config(
            "warning", background="#fffa65", selectbackground="black"
        )
        self.textBox.tag_config("error", background="#e74c3c", selectbackground="black")
        self.textBox.tag_config(
            "control", background="#2ecc71", selectbackground="black"
        )
        self.textBox.tag_config("basic", background="white", selectbackground="black")

        logoutButton = tk.Button(self.root)
        logoutButton["bg"] = "#efefef"
        ft = tkFont.Font(family=self.fontFamily, size=10)
        logoutButton["font"] = ft
        logoutButton["fg"] = "#000000"
        logoutButton["justify"] = "center"
        logoutButton["text"] = "logout"
        logoutButton.place(x=55, y=270, width=70, height=25)
        logoutButton["command"] = self.logout

    def authenticate(self):
        n_email = self.email_entry.get()
        n_password = self.password_entry.get()
        users = db.get("/PaladinsUsers")
        emailCheck = False
        passwordCheck = False
        for user in users:
            if n_email == user["Email"]:
                emailCheck = True
            if n_password == user["Password"]:
                passwordCheck = True
            if emailCheck and passwordCheck:
                endDate = user["enddate"]
                currentDate = datetime.datetime.now()
                date_format = "%Y-%m-%dT%H:%M:%SZ"
                date_obj = datetime.datetime.strptime(endDate, date_format)
                if endDate > currentDate:
                    self.email_error = tk.Label(self.root)
                    self.email_error["text"] = "Ops! Key has ran out"
                    ft = tkFont.Font(family=self.fontFamily, size=10)
                    self.email_error["font"] = ft
                    self.email_error["fg"] = "#ff0000"
                    self.email_error.place(x=130, y=340, width=267, height=15)
                    return False
                else:
                    return True
            else:
                n_email = False
                n_password = False
        self.email_error = tk.Label(self.root)
        self.email_error["text"] = "Invalid login. please try again"
        ft = tkFont.Font(family=self.fontFamily, size=10)
        self.email_error["font"] = ft
        self.email_error["fg"] = "#ff0000"
        self.email_error.place(x=130, y=220, width=267, height=15)
        return False

    def login_btn_command(self):
        # self.login=self.authenticate()
        # self.login=True
        if self.authenticate() == True:
            self.clear()
            width = 1600
            height = 700
            screenwidth = self.root.winfo_screenwidth()
            screenheight = self.root.winfo_screenheight()
            alignstr = "%dx%d+%d+%d" % (
                width,
                height,
                (screenwidth - width) / 2,
                (screenheight - height) / 2,
            )
            self.root.geometry(alignstr)
            self.root.resizable(width=False, height=False)

            self.lastMessage = None
            self.fontFamily = "Calibri"

            self.startButton = tk.Button(self.root)
            self.startButton["bg"] = "#41c42d"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            self.startButton["font"] = ft
            self.startButton["fg"] = "#000000"
            self.startButton["justify"] = "center"
            self.startButton["text"] = "Start"
            self.startButton["state"] = "normal"
            self.startButton.place(x=40, y=50, width=100, height=40)
            self.startButton["command"] = self.startBot

            self.stopButton = tk.Button(self.root)
            self.stopButton["bg"] = "#ff0000"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            self.stopButton["font"] = ft
            self.stopButton["fg"] = "#000000"
            self.stopButton["justify"] = "center"
            self.stopButton["text"] = "Stop"
            self.stopButton["state"] = "disabled"
            self.stopButton.place(x=40, y=120, width=100, height=40)
            self.stopButton["command"] = self.stopBot

            self.textBox = tk.Text(self.root)
            self.textBox["borderwidth"] = "1px"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            self.textBox["font"] = ft
            self.textBox["fg"] = "#333333"
            self.textBox.place(x=180, y=50, width=520, height=260)
            self.textBox.tag_config(
                "warning", background="#fffa65", selectbackground="black"
            )
            self.textBox.tag_config(
                "error", background="#e74c3c", selectbackground="black"
            )
            self.textBox.tag_config(
                "control", background="#2ecc71", selectbackground="black"
            )
            self.textBox.tag_config(
                "basic", background="white", selectbackground="black"
            )

            logoutButton = tk.Button(self.root)
            logoutButton["bg"] = "#efefef"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            logoutButton["font"] = ft
            logoutButton["fg"] = "#000000"
            logoutButton["justify"] = "center"
            logoutButton["text"] = "logout"
            logoutButton.place(x=55, y=270, width=70, height=25)
            logoutButton["command"] = self.logout

            settingsFrame = tk.LabelFrame(self.root)
            settingsFrame["borderwidth"] = "1px"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            settingsFrame["font"] = ft
            settingsFrame["fg"] = "#333333"
            settingsFrame["text"] = "Settings"
            settingsFrame.place(x=720, y=40, width=350, height=305)

            saveButton = tk.Button(self.root)
            saveButton["bg"] = "#efefef"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            saveButton["font"] = ft
            saveButton["fg"] = "#000000"
            saveButton["justify"] = "center"
            saveButton["text"] = "Save Log"
            saveButton.place(x=630, y=330, width=70, height=25)
            saveButton["command"] = self.saveText
            clearButton = tk.Button(self.root)
            clearButton["bg"] = "#efefef"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            clearButton["font"] = ft
            clearButton["fg"] = "#000000"
            clearButton["justify"] = "center"
            clearButton["text"] = "Clear Log"
            clearButton.place(x=540, y=330, width=70, height=25)
            clearButton["command"] = self.clearText

            self.screenshotCheckVal = tk.IntVar()
            self.screenshotCheck = tk.Checkbutton(self.root)
            ft = tkFont.Font(family=self.fontFamily, size=10)
            self.screenshotCheck["font"] = ft
            self.screenshotCheck["fg"] = "#333333"
            self.screenshotCheck["justify"] = "left"
            self.screenshotCheck[
                "text"
            ] = "Save screenshots of Match Stats to your computer"
            self.screenshotCheck.place(x=745, y=150, width=300, height=25)
            self.screenshotCheck["offvalue"] = "0"
            self.screenshotCheck["onvalue"] = "1"
            self.screenshotCheck["variable"] = self.screenshotCheckVal

            pushbulletFrame = tk.LabelFrame(self.root)
            pushbulletFrame["borderwidth"] = "1px"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            pushbulletFrame["font"] = ft
            pushbulletFrame["fg"] = "#333333"
            pushbulletFrame["text"] = "Pushbullet"
            pushbulletFrame.place(x=730, y=190, width=335, height=120)

            self.pushCheckVal = tk.IntVar()
            self.pushCheck = tk.Checkbutton(self.root)
            ft = tkFont.Font(family=self.fontFamily, size=10)
            self.pushCheck["font"] = ft
            self.pushCheck["fg"] = "#333333"
            self.pushCheck["justify"] = "center"
            self.pushCheck["text"] = "Push screenshots of Match Stats with Pushbullet"
            self.pushCheck.place(x=745, y=205, width=284, height=30)
            self.pushCheck["offvalue"] = 0
            self.pushCheck["onvalue"] = 1
            self.pushCheck["variable"] = self.pushCheckVal

            """self.btnShowFlank = tk.Button(self.root)
            self.btnShowFlank["text"] = "Pick Flanker"
            self.btnShowFlank["command"] = self.showAttackScroll
            self.btnShowFlank.place(x=90, y=180, width=161, height=41)"""

            self.btnShowSupport = tk.Button(self.root)
            self.btnShowSupport["text"] = "Pick Support"
            self.btnShowSupport["command"] = self.showSupportScroll
            self.btnShowSupport.place(x=50, y=180, width=90, height=30)

            self.token = tk.Entry(self.root)
            self.token["borderwidth"] = "1px"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            self.token["font"] = ft
            self.token["fg"] = "#333333"
            self.token["justify"] = "center"
            self.token["text"] = ""
            self.token.place(x=735, y=255, width=290, height=30)

            testButton = tk.Button(self.root)
            testButton["bg"] = "#efefef"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            testButton["font"] = ft
            testButton["fg"] = "#000000"
            testButton["justify"] = "center"
            testButton["text"] = "test"
            testButton.place(x=1030, y=255, width=30, height=32)
            testButton["command"] = self.pbSendTestMessage

            tokenLabel = tk.Label(self.root)
            ft = tkFont.Font(family=self.fontFamily, size=10)
            tokenLabel["font"] = ft
            tokenLabel["fg"] = "#333333"
            tokenLabel["justify"] = "left"
            tokenLabel["text"] = "Insert your Access Token below:"
            tokenLabel.place(x=738, y=225, width=326, height=30)

            resetButton = tk.Button(self.root)
            resetButton["bg"] = "#efefef"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            resetButton["font"] = ft
            resetButton["fg"] = "#000000"
            resetButton["justify"] = "center"
            resetButton["text"] = "Reset saved settings "
            resetButton.place(x=940, y=310, width=118, height=30)
        else:
            self.email_error = tk.Label(self.root)
            self.email_error["text"] = "invalid login. please try again"
            ft = tkFont.Font(family=self.fontFamily, size=10)
            self.email_error["font"] = ft
            self.email_error["fg"] = "#ff0000"
            self.email_error.place(x=130, y=220, width=267, height=15)

    def startBot(self):
        if self.tier == 0:
            self.mainbot = mainbotloop.mainLoop(
                self.textBox, (0, 25), False, False, 0, False, tier=self.tier, times=0
            )
        else:
            statsBool = self.screenshotCheckVal.get()
            pbBool = self.pushCheckVal.get()
            pbAccTkn = self.token.get()
            self.mainbot = mainbotloop.mainLoop(
                self.textBox,
                (2, 4),
                statsBool,
                pbBool,
                pbAccTkn,
                False,
                tier=self.tier,
                times=0,
            )
        if not self.mainbot.invalid:
            if self.mainbot.startLoop():
                self.startButton["state"] = "disabled"
                self.stopButton["state"] = "normal"

    def stopBot(self):
        self.stopButton["state"] = "disabled"
        self.startButton["state"] = "normal"
        self.mainbot.stopLoop()

    def clearText(self):
        self.textBox.configure(state="normal")
        self.textBox.delete("1.0", END)
        self.textBox.configure(state="disabled")
        self.isTextBoxClear = True

    def saveText(self):
        self.textBox.configure(state="normal")
        textToSave = self.textBox.get("1.0", END)
        file_path = filedialog.asksaveasfilename(
            initialdir=(os.path.dirname(os.path.realpath(__file__))),
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        try:
            with open(file_path, "w") as (f):
                f.write(textToSave)
        except EnvironmentError:
            self.print_to_GUI("Could not save file. Please try again")

    def showLoginFrame(self):
        self.clear()
        width = 500
        height = 250
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        self.title_label.place(x=140, y=10, width=219, height=69)
        self.email_label.place(x=50, y=100, width=70, height=25)
        self.email_entry.place(x=130, y=90, width=267, height=42)
        self.rembr_chkbx.place(x=180, y=140, width=167, height=30)
        self.login_btn.place(x=180, y=180, width=161, height=41)

    def logout(self):
        self.showLoginFrame()
        if self.mainbot is not None:
            self.stopBot()
            self.mainbot = None
        self.startButton["state"] = "normal"
        self.stopButton["state"] = "disabled"

    def pbSendTestMessage(self):
        url = "https://api.pushbullet.com/v2/pushes"
        headers = {"Access-Token": self.token.get()}
        data = {
            "type": "note",
            "title": "FortBot Pushbullet test",
            "body": "1, 2, 3 ... all set!",
        }
        res = requests.post(url, json=data, headers=headers)
        if res.status_code != 200 or self.token.get() == "":
            self.print_to_GUI("Incorrect Access Token for Pushbullet", "error")
        else:
            self.print_to_GUI("Pushbullet test successful")

    def print_to_GUI(self, msg, type="basic"):
        if msg == self.lastMessage and not self.isTextBoxClear:
            return
        self.textBox.configure(state="normal")
        autoscroll = False
        ts = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y/%m/%d %H:%M:%S || "
        )
        if self.textBox.yview()[1] == 1:
            autoscroll = True
        self.textBox.insert(END, ts + msg + "\n", type)
        self.lastMessage = msg
        if autoscroll:
            self.textBox.see(END)
        self.textBox.configure(state="disabled")
        self.isTextBoxClear = False


if __name__ == "__main__":
    login = App()
