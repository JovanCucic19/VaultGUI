import Tkinter as tk
from pexpect import pxssh
import getpass

class EnergyGUI(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=600, height=500)
        master.after(1000, self.run_vault)

        # self.pack_propagate(0)
        self.master.title("Energy GUI")

        self.accept_button = tk.Button(
            self, text="accept",
            height=7, width=20
        ).grid(row=0, column=0)

        self.reject_button = tk.Button(
            self, text="reject",
            height=7, width=20
        ).grid(row=0,column=1)

        self.console_log = tk.Text(
            self, height=15, width=100
        )
        self.console_log.grid(row=1, column=0, rowspan=6, columnspan=2)

        # self.tk.after(100)
        self.pack()


#       OBRISATI BASH HISTORY NAKON IZLOGOVANJA
#
#
    def run_vault(self):
        s = pxssh.pxssh(timeout=3)
        s.login('127.0.0.1', 'vagrant', 'vagrant',port='2222')
        # s.sendline('ls')
        # s.prompt()
        # print s.before
        print("connection created!")
        s.sendline('cd /code')
        s.prompt()
        print(s.before)
        self.console_log.insert(tk.END, s.before)

        s.sendline('ls')
        s.prompt()
        print(s.before)
        self.console_log.insert(tk.END, s.before)

        s.sendline('python vault.py')
        s.prompt()
        print(s.before)
        # print("Waiting for pass")
        self.console_log.insert(tk.END, s.before)

        s.sendline('vagrant')
        s.prompt()
        print(s.before)
        self.console_log.insert(tk.END, s.before)

    def run(self):
        self.mainloop()



if __name__ == '__main__':
    app = EnergyGUI(tk.Tk())
    app.run()
