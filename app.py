import Tkinter as tk
from pexpect import pxssh
import getpass
import threading
import time

class EnergyGUI(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=600, height=500)

        self.master.title("Energy GUI")

        self.accept_button = tk.Button(
            self, text="accept",
            height=7, width=20,
            command=self.password_prompt, state=tk.DISABLED
        )
        self.accept_button.grid(row=0, column=0)

        self.reject_button = tk.Button(
            self, text="reject",
            height=7, width=20, state=tk.DISABLED
        )
        self.reject_button.grid(row=0, column=1)

        self.console_log = tk.Text(
            self, height=15, width=100, state=tk.DISABLED
        )
        self.console_log.grid(row=1, column=0, rowspan=6, columnspan=2)

        # self.tk.after(100)
        self.pack()
        self.password_prompt()

    def password_prompt(self):
        self.toplevel = tk.Toplevel()
        self.toplevel.minsize(width=400, height=200)
        self.toplevel.protocol('WM_DELETE_WINDOW', self.destroy_parent_window)

        self.center(self.toplevel)

        self.password_label = tk.Label(
            self.toplevel, text="Enter password", height=2, width=20
            )
        self.password_label.pack()
        self.master.withdraw()
        self.password_text = tk.Text(self.toplevel,
            height=1, width=20
        )
        self.password_text.pack()
        self.password_text.focus_set()

        self.password_button = tk.Button(
            self.toplevel, text="Enter",
            height=3, width=10, command= lambda: self.get_password(self.password_text)
        )
        self.password_button.pack()

        self.connecting_label = tk.Label(
            self.toplevel,
            height=3, width=10
        )
        self.connecting_label.pack()

    def destroy_parent_window(self):
        self.master.destroy()

    def get_password(self, password_text):
        password_tmp = password_text.get("1.0", 'end-1c')

        if password_tmp == "vagrant":

            self.console_log.config(state=tk.NORMAL)
            self.accept_button.config(state=tk.NORMAL)
            self.reject_button.config(state=tk.NORMAL)

            t = threading.Thread(target=self.run_vault)
            t.start()

            while (t.is_alive()):
                time.sleep(3)
                print("Am i alive? {}".format(t.is_alive()))

            self.master.deiconify()
            self.toplevel.withdraw()


            print(self.accept_button['state'])
        print(password_tmp)



    def center(self, toplevel):
        ws = toplevel.winfo_screenwidth()
        hs = toplevel.winfo_screenheight()
        wtop = 300
        htop = 300
        x = ws/2 - wtop/2
        y = hs/2 - htop/2
        toplevel.geometry("%dx%d+%d+%d" %  (wtop, htop, x, y))

#       OBRISATI BASH HISTORY NAKON IZLOGOVANJA
#
#
    def run_vault(self):
        s = pxssh.pxssh(timeout=3)
        s.login('127.0.0.1', 'vagrant', 'vagrant', port='2222')
        # s.sendline('ls')
        # s.prompt()
        # print s.before
        print("connection created!")
        s.sendline('cd /code')
        s.prompt()
        print(s.before)
        # self.console_log.insert(tk.END, s.before)

        s.sendline('ls')
        s.prompt()
        print(s.before)
        #self.console_log.insert(tk.END, s.before)

        s.sendline('python vault.py')
        s.prompt()
        print(s.before)
        #self.console_log.insert(tk.END, s.before)

        # vault_password = self.password_text.get("1.0", 'end-1c')
        s.sendline('vagrant')
        s.prompt()
        print(s.before)
        #self.console_log.insert(tk.END, s.before)

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    app = EnergyGUI(tk.Tk())
    app.run()
