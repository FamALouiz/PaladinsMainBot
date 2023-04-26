from tkinter import *
from tkinter import filedialog
from tkinter import font
import mainBotLoop, asyncio, threading, time, uuid, winreg, datetime, os, sys, ssl
import pyautogui
from PIL import *

""" iterator = PositionableSequenceIterator(
            [[a, b, c] for a, b, c in zip(btnlist2.keys(), btnlist2.values(), icons2)]
        )"""

iconlistGrover = [
    os.path.join(r"PaladinMainbot_pngs\Grover", f)
    for f in os.listdir(r"PaladinMainbot_pngs\Grover")
    if f.endswith(".png")
]


iconsGrover = [
    r"PaladinMainbot_pngs\Grover" + "/" + f
    for f in os.listdir(r"PaladinMainbot_pngs\Grover")
]


class PositionableSequenceIterator:
    def __init__(self, sequence):
        self.seq = sequence
        self._nextpos = 0

    @property
    def pos(self):
        pos = self._nextpos
        return 0 if pos is None else pos - 1

    @pos.setter
    def pos(self, newpos):
        if not 0 <= newpos < len(self.seq):
            raise IndexError(newpos)
        self._nextpos = newpos

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.seq[self._nextpos or 0]
        except IndexError:
            raise StopIteration
        finally:
            self._nextpos += 1


def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)


import requests


class BotGUI:
    def __init__(self):
        self.initRegEntries()
        self.root = Tk()
        self.root.title(str(uuid.uuid4())[:8])
        self.root.iconbitmap(resource_path("bot_icon.ico"))
        self.greenColor = "#2ecc71"
        self.redColor = "#e74c3c"
        self.yellowColor = "#fffa65"
        self.purpleColor = "#6b42f4"
        self.bigFont = font.Font(
            family="Franklin Gothic Medium", size=14, weight="bold"
        )
        self.bot = None
        self.botTask = None
        self.emailInput = StringVar()
        self.lastLoginTime = 0
        self.lastMessage = ""
        self.loginFrame = Frame((self.root), pady=30, padx=30)
        self.initLoginFrame()
        self.mainFrame = Frame((self.root), pady=30, padx=30)
        self.showLoginFrame()
        self.root.mainloop()
        self.sbFlank = Scrollbar()
        self.sbFlank.pack_forget()
        self.sbSupport = Scrollbar()
        self.sbSupport.pack_forget()

    def initRegEntries(self):
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Software\\FortBot", 0, winreg.KEY_READ
            )
            value, _ = winreg.QueryValueEx(key, "esc_button_scale")
            value, _ = winreg.QueryValueEx(key, "continue_button_scale")
            value, _ = winreg.QueryValueEx(key, "collect_button_scale")
            value, _ = winreg.QueryValueEx(key, "play_button_scale")
            value, _ = winreg.QueryValueEx(key, "return_button_scale")
            value, _ = winreg.QueryValueEx(key, "icons_scale")
            value, _ = winreg.QueryValueEx(key, "team_alive_scale")
            value, _ = winreg.QueryValueEx(key, "remember_login")
            value, _ = winreg.QueryValueEx(key, "login_email")
            value, _ = winreg.QueryValueEx(key, "land_on_trees")
            value, _ = winreg.QueryValueEx(key, "take_ss_local")
            value, _ = winreg.QueryValueEx(key, "send_ss_pb")
            value, _ = winreg.QueryValueEx(key, "pb_acc_token")
            winreg.CloseKey(key)
        except WindowsError:
            self.resetRegEntries()

    def resetRegEntries(self):
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\FortBot")
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "Software\\FortBot", 0, winreg.KEY_WRITE
            )
            winreg.SetValueEx(
                registry_key, "esc_button_scale", 0, winreg.REG_SZ, str(-1)
            )
            winreg.SetValueEx(
                registry_key, "continue_button_scale", 0, winreg.REG_SZ, str(-1)
            )
            winreg.SetValueEx(
                registry_key, "collect_button_scale", 0, winreg.REG_SZ, str(-1)
            )
            winreg.SetValueEx(
                registry_key, "play_button_scale", 0, winreg.REG_SZ, str(-1)
            )
            winreg.SetValueEx(
                registry_key, "return_button_scale", 0, winreg.REG_SZ, str(-1)
            )
            winreg.SetValueEx(registry_key, "icons_scale", 0, winreg.REG_SZ, str(-1))
            winreg.SetValueEx(
                registry_key, "team_alive_scale", 0, winreg.REG_SZ, str(-1)
            )
            winreg.SetValueEx(registry_key, "remember_login", 0, winreg.REG_SZ, "off")
            winreg.SetValueEx(registry_key, "login_email", 0, winreg.REG_SZ, "")
            winreg.SetValueEx(registry_key, "land_on_trees", 0, winreg.REG_SZ, "off")
            winreg.SetValueEx(registry_key, "take_ss_local", 0, winreg.REG_SZ, "off")
            winreg.SetValueEx(registry_key, "send_ss_pb", 0, winreg.REG_SZ, "off")
            winreg.SetValueEx(registry_key, "pb_acc_token", 0, winreg.REG_SZ, "")
            winreg.CloseKey(registry_key)
        except WindowsError:
            print("Error resetting registry entries.")

    def initLoginFrame(self):
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Software\\FortBot", 0, winreg.KEY_READ
        )
        labelLogin = Label(
            (self.loginFrame), text="FortBot - Log in", font=("Calibri", 24)
        )
        emailFrame = Frame(self.loginFrame)
        labelEmail = Label(emailFrame, text="Email ", font=("Calibri", 14))
        self.entryEmail = Entry(
            emailFrame, font=("Calibri", 14), textvariable=(self.emailInput)
        )
        underEmailFrame = Frame(self.loginFrame)
        self.btnLogin = Button(
            underEmailFrame,
            text="Login",
            font=(self.bigFont),
            fg="white",
            bg=(self.purpleColor),
        )
        self.btnLogin.bind("<Button-1>", self.login)
        self.rememberLoginInt = IntVar()
        btnRememberLogin = Checkbutton(
            underEmailFrame,
            text="Remember me",
            font=("Calibri", 12),
            variable=(self.rememberLoginInt),
        )
        value, _ = winreg.QueryValueEx(key, "remember_login")
        if value == "on":
            btnRememberLogin.select()
            value, _ = winreg.QueryValueEx(key, "login_email")
            self.entryEmail.insert(0, value)
        self.btnFreeTrial = Button(
            (self.loginFrame),
            text="Free Trial",
            font=("Calibri", 14, "bold"),
            bg=(self.yellowColor),
        )
        self.btnFreeTrial.bind("<Button-1>", self.login)
        self.labelLoginError = Label(
            (self.loginFrame), text="", font=("Calibri", 8), fg="red"
        )
        labelLogin.grid(row=0, column=0, pady=(0, 20))
        emailFrame.grid(row=1, column=0, sticky=(NE + SW), pady=10)
        labelEmail.grid(row=0, column=0, sticky=E)
        self.entryEmail.grid(row=0, column=1)
        underEmailFrame.grid(row=2, column=0, sticky=(NE + SW), pady=2)
        underEmailFrame.columnconfigure(1, weight=1)
        btnRememberLogin.grid(row=0, column=0, sticky=NW)
        self.btnLogin.grid(row=0, column=1, sticky=E, pady=10)
        self.btnFreeTrial.grid(row=3, sticky=E)
        self.labelLoginError.grid(row=4, pady=(10, 0))
        winreg.CloseKey(key)

    def initMainFrame(self, tier):
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Software\\FortBot", 0, winreg.KEY_READ
        )
        scBarLogger = Scrollbar((self.mainFrame), orient=VERTICAL)
        self.listBoxLogger = Text(
            (self.mainFrame),
            state="disabled",
            height=15,
            width=70,
            yscrollcommand=(scBarLogger.set),
            selectbackground="black",
            font=("-*-lucidatypewriter-medium-r-*-*-*-140-*-*-*-*-*-*", 14),
        )
        self.listBoxLogger.tag_config(
            "warning", background=(self.yellowColor), selectbackground="black"
        )
        self.listBoxLogger.tag_config(
            "error", background=(self.redColor), selectbackground="black"
        )
        self.listBoxLogger.tag_config(
            "control", background=(self.greenColor), selectbackground="black"
        )
        self.listBoxLogger.tag_config(
            "basic", background="white", selectbackground="black"
        )
        scBarLogger.config(command=(self.listBoxLogger.yview))
        botControlFrame = Frame(self.mainFrame)
        botControlFrame.rowconfigure(2, weight=1)
        self.btnStart = Button(
            botControlFrame,
            text="START",
            bg=(self.greenColor),
            font=(self.bigFont),
            command=(self.startBot),
        )
        self.btnStop = Button(
            botControlFrame,
            state="disabled",
            text="STOP",
            bg=(self.redColor),
            font=(self.bigFont),
            command=(self.stopBot),
        )
        btnLogout = Button(botControlFrame, text="Logout", command=(self.logout))
        self.listBoxLogger.grid(row=0, column=1)
        scBarLogger.grid(row=0, column=2, sticky=(N + S + W))
        botControlFrame.grid(row=0, column=0, sticky=(NE + SW))
        self.btnStart.grid(row=0, column=0, pady=10, padx=10, sticky=N)
        self.btnStop.grid(row=1, column=0, pady=10, padx=10, sticky=N)
        btnLogout.grid(row=2, column=0, pady=10, padx=10, sticky=S)
        botLogFrame = Frame(self.mainFrame)
        self.btnClearLog = Button(
            botLogFrame, text="Clear Log", command=(self.clearLog)
        )
        self.btnSaveLog = Button(botLogFrame, text="Save Log", command=(self.saveLog))
        optionsFrame = LabelFrame((self.mainFrame), text="Settings")
        self.btnResetScale = Button(
            optionsFrame, text="Reset saved settings", command=(self.resetSettings)
        )
        busJumpFrame = Frame(optionsFrame)
        busJumpFrame.columnconfigure(0, weight=1)
        busJumpFrame.columnconfigure(4, weight=1)
        lblBusJump1 = Label(busJumpFrame, text="Pick a Champion from the buttons above")
        self.treesInt = IntVar()
        self.statsSSInt = IntVar()
        statsSSchkbtn = Checkbutton(
            optionsFrame,
            text="Save screenshots of Match Stats to your computer",
            variable=(self.statsSSInt),
        )
        value, _ = winreg.QueryValueEx(key, "take_ss_local")
        if value == "on":
            statsSSchkbtn.select()
        pushbulletFrame = LabelFrame(optionsFrame, text="Pushbullet")
        self.pushbulletInt = IntVar()
        pbchkbtn = Checkbutton(
            pushbulletFrame,
            text="Push screenshots of Match Stats with Pushbullet",
            variable=(self.pushbulletInt),
        )
        value, _ = winreg.QueryValueEx(key, "send_ss_pb")
        if value == "on":
            pbchkbtn.select()
        self.accToken = StringVar()
        labelAccToken = Label(pushbulletFrame, text="Insert your Access Token below:")
        self.entryAccToken = Entry(
            pushbulletFrame, width=40, show="*", textvariable=(self.accToken)
        )
        value, _ = winreg.QueryValueEx(key, "pb_acc_token")
        self.entryAccToken.insert(0, value)
        self.btnPbTest = Button(
            pushbulletFrame, text="Test", command=(self.pbSendTestMessage)
        )
        btnShowFlank = Button(text="Pick Flanker", command=self.showAttackScroll)
        btnShowSupport = Button(text="Pick Support", command=self.showSupportScroll)
        if tier >= 1:
            botLogFrame.grid(row=3, column=1, sticky=E)
            self.btnClearLog.grid(row=0, column=0, pady=10, padx=10, sticky=E)
            self.btnSaveLog.grid(row=0, column=1, pady=10, padx=10, sticky=W)
            optionsFrame.grid(row=0, column=3, padx=10, sticky=N)
            self.btnResetScale.grid(row=4, column=0, pady=10, padx=10, sticky=E)
            busJumpFrame.grid(row=0, column=0, sticky=N)
            lblBusJump1.grid(row=0, column=0, columnspan=5)
            statsSSchkbtn.grid(row=2, column=0, pady=0, sticky=N)
            pushbulletFrame.grid(row=3, column=0)
            pbchkbtn.grid(row=0, columnspan=2)
            labelAccToken.grid(row=1, column=0, sticky=W)
            self.entryAccToken.grid(row=2, column=0, pady=(0, 10))
            self.btnPbTest.grid(row=2, column=1, pady=(0, 10))
            btnShowFlank.grid(row=2, column=0)
            btnShowSupport.grid(row=1, column=0)

        winreg.CloseKey(key)

    def resetSettings(self):
        self.resetRegEntries()
        self.initMainFrame(self.tier)

    def showAttackScroll(self):
        text = Text(self.root)
        text.grid(row=2, column=1)
        self.sbFlank = Scrollbar(self.root, command=text.yview)
        self.sbFlank.grid(row=2, column=1)
        text.configure(yscrollcommand=self.sbFlank.set)
        for i in range(10):
            button = Button(text)
            text.window_create("end", window=button)
            text.insert("end", "\n")
        text.configure(state="disabled")

    def showSupportScroll(self):
        text = Text(self.root)
        text.grid(row=2, column=1)
        self.sbSupport = Scrollbar(self.root, command=text.yview)
        self.sbSupport.grid(row=2, column=1)
        text.configure(yscrollcommand=self.sbSupport.set)
        button = Button(text="Groove", command=self.pickSupportGroove)
        text.window_create("end", window=button)
        text.insert("end", "\n")
        for i in range(11):
            button = Button(text)
            text.window_create("end", window=button)
            text.insert("end", "\n")
        text.configure(state="disabled")

    def pickSupportGroove(self):
        iterator = PositionableSequenceIterator(
            [[a, b] for a, b in zip(iconlistGrover, iconsGrover)]
        )
        flag = True
        while flag:
            for i in iterator:
                icon = i[0]
                try:
                    pyautogui.click(
                        pyautogui.center(pyautogui.locateOnScreen(icon, confidence=0.9))
                    )
                    self.print_to_GUI(f"Found {icon}")
                except:
                    self.print_to_GUI(f"Checking next png")
                else:
                    flag = False
                time.sleep(4)

        self.print_to_GUI(f"Done Grove")

    def clickFlankChampion(self):
        print("TEST2")

    def showLoginFrame(self):
        self.loginFrame.grid()
        self.mainFrame.grid_forget()
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() // 2 - self.root.winfo_width() // 2
        y = self.root.winfo_screenheight() // 2 - self.root.winfo_height() // 2
        self.root.geometry("+%d+%d" % (x, y))

    def showMainFrame(self):
        self.loginFrame.grid_forget()
        self.mainFrame.grid()
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() // 2 - self.root.winfo_width() // 2
        y = self.root.winfo_screenheight() // 2 - self.root.winfo_height() // 2
        self.root.geometry("+%d+%d" % (x, y))

    def clearLog(self):
        self.listBoxLogger.configure(state="normal")
        self.listBoxLogger.delete("1.0", END)
        self.listBoxLogger.configure(state="disabled")

    def saveLog(self):
        self.listBoxLogger.configure(state="normal")
        textToSave = self.listBoxLogger.get("1.0", END)
        file_path = filedialog.asksaveasfilename(
            initialdir=(os.path.dirname(os.path.realpath(__file__))),
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        try:
            with open(file_path, "w") as (f):
                f.write(textToSave)
        except EnvironmentError:
            print("Cannot save file.")

        self.listBoxLogger.configure(state="disabled")

    def login(self, event):
        if event.widget == self.btnLogin:
            dur = time.time() - self.lastLoginTime
            if dur < 10.0:
                self.labelLoginError["text"] = (
                    "Please wait "
                    + "%.0f" % (10.0 - dur)
                    + " seconds before your next login attempt."
                )
                return
            self.lastLoginTime = time.time()
            email = self.emailInput.get()
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Software\\Epic Games\\Unreal Engine\\Identifiers",
                0,
                winreg.KEY_READ,
            )
            id1, _ = winreg.QueryValueEx(key, "MachineId")
            winreg.CloseKey(key)
            self.tier = self.authenticate(email, id1)
            if self.tier == -1:
                self.labelLoginError["text"] = "Invalid email or device."
            else:
                registry_key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, "Software\\FortBot", 0, winreg.KEY_WRITE
                )
                if self.rememberLoginInt.get() == 1:
                    winreg.SetValueEx(
                        registry_key, "remember_login", 0, winreg.REG_SZ, "on"
                    )
                    winreg.SetValueEx(
                        registry_key, "login_email", 0, winreg.REG_SZ, email
                    )
                else:
                    winreg.SetValueEx(
                        registry_key, "remember_login", 0, winreg.REG_SZ, "off"
                    )
                    winreg.SetValueEx(registry_key, "login_email", 0, winreg.REG_SZ, "")
                winreg.CloseKey(registry_key)
                self.initMainFrame(self.tier)
                self.showMainFrame()
        else:
            if event.widget == self.btnFreeTrial:
                self.tier = 0
                self.resetRegEntries()
                self.initMainFrame(self.tier)
                self.showMainFrame()
            else:
                self.labelLoginError["text"] = "Invalid action."

    def authenticate(self, email, myid):
        # payload = {'email':email,  'uuid':myid}
        # r = requests.post('https://fortbot-server.herokuapp.com/users', data=payload)
        # jsonAns = r.json()
        return 3  # jsonAns['tier']

    def startBot(self):
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Software\\FortBot", 0, winreg.KEY_WRITE
        )
        landOnTreesBool = self.treesInt.get() == 1
        statsBool = self.statsSSInt.get() == 1
        pbBool = self.pushbulletInt.get() == 1
        pbAccTkn = self.accToken.get()
        winreg.SetValueEx(
            registry_key,
            "land_on_trees",
            0,
            winreg.REG_SZ,
            "on" if landOnTreesBool else "off",
        )
        winreg.SetValueEx(
            registry_key,
            "take_ss_local",
            0,
            winreg.REG_SZ,
            "on" if statsBool else "off",
        )
        winreg.SetValueEx(
            registry_key, "send_ss_pb", 0, winreg.REG_SZ, "on" if pbBool else "off"
        )
        winreg.SetValueEx(registry_key, "pb_acc_token", 0, winreg.REG_SZ, pbAccTkn)
        self.bot = mainBotLoop.MainBotLoop(
            self.listBoxLogger,
            statsBool,
            pbBool,
            pbAccTkn,
            landOnTreesBool,
            self.tier,
        )
        if self.bot.startLoop(lambda: self.enableStart(self.btnStart, self.btnStop)):
            self.btnStart["state"] = "disabled"
            self.btnStop["state"] = "normal"
        winreg.CloseKey(registry_key)

    def stopBot(self):
        self.btnStop["state"] = "disabled"
        self.bot.stopLoop()

    def enableStart(self, btnS, btnE):
        btnS["state"] = "normal"
        btnE["state"] = "disabled"

    def logout(self):
        self.showLoginFrame()
        if self.bot is not None:
            self.stopBot()
            self.bot = None
        self.btnStart["state"] = "normal"
        self.btnStop["state"] = "disabled"

    def pbSendTestMessage(self):
        url = "https://api.pushbullet.com/v2/pushes"
        headers = {"Access-Token": self.accToken.get()}
        data = {
            "type": "note",
            "title": "FortBot Pushbullet test",
            "body": "1, 2, 3 ... all set!",
        }
        res = requests.post(url, json=data, headers=headers)
        if res.status_code != 200 or self.accToken.get() == "":
            self.print_to_GUI("Incorrect Access Token for Pushbullet", "error")
        else:
            self.print_to_GUI("Pushbullet test successful")

    def print_to_GUI(self, msg, type="basic"):
        if msg == self.lastMessage:
            return
        self.listBoxLogger.configure(state="normal")
        autoscroll = False
        ts = datetime.datetime.fromtimestamp(time.time()).strftime(
            "%Y/%m/%d %H:%M:%S || "
        )
        if self.listBoxLogger.yview()[1] == 1:
            autoscroll = True
        self.listBoxLogger.insert(END, ts + msg + "\n", type)
        self.lastMessage = msg
        if autoscroll:
            self.listBoxLogger.see(END)
        self.listBoxLogger.configure(state="disabled")

    def main_file_path(self):
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    bGUI = BotGUI()
