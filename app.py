import Tkinter as tk
from pexpect import pxssh
from tkMessageBox import showinfo, showerror, askokcancel
import threading
import getpass
import time
import config


def connect_via_ssh(ssh_ip, ssh_username, ssh_key_path, ssh_port):
    connection = pxssh.pxssh(timeout=3)
    print('Trying to connect')
    connection.login(ssh_ip, ssh_username, ssh_key=ssh_key_path, port=ssh_port)
    print('Connected')


def password_incorrect_window():
    password_expired_window_title = "Password Incorrect"
    password_expired_window_message = "I am sorry master, the password is incorrect"
    showerror(password_expired_window_title, password_expired_window_message)


class EnergyGUI(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=600, height=500)

        self.master.title("Energy GUI")
        self.master.protocol("WM_DELETE_WINDOW", self.destroy_parent_window)

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

        self.password_text = tk.Entry(self.toplevel, show="*")
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
        if askokcancel("Quit", "You want to leave me Master? *sniff*"):

            self.master.destroy()


    def get_password(self, password_text):
        # password_tmp = password_text.get("1.0", 'end-1c')
        password_tmp = password_text.get()

        # if password_tmp == config.tmp_login_password:

        self.console_log.config(state=tk.NORMAL)
        self.accept_button.config(state=tk.NORMAL)
        self.reject_button.config(state=tk.NORMAL)

        print('Preparing to run Vault on ssh')
        try:
            t = threading.Thread(target=self.run_vault(password_tmp))
            t.start()


            while (t.is_alive()):
                time.sleep(3)
                print("Am i alive? {}".format(t.is_alive()))
            self.master.deiconify()
            self.toplevel.withdraw()
        except:
            print("Bad wallet password")
            password_incorrect_window()


        # else:
        #     password_incorrect_window()


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
    def run_vault(self, password_text):
        try:
            s = pxssh.pxssh(timeout=3)
            s.login(config.ssh_ip, config.ssh_username, ssh_key=config.ssh_key_path, port=config.ssh_port)
            # PROMPT = p.PROMPT
            print("Connection created!")
            # s = connect_via_ssh(config.ssh_ip, config.ssh_username, config.ssh_key_path, config.ssh_port)

            # s.sendline('ls')
            # s.prompt()
            # print s.before

            print('Entering Vault dir')
            s.sendline('cd /code')
            s.prompt()
            # print(s.before)
            # self.console_log.insert(tk.END, s.before)

            # s.sendline('ls')
            # s.prompt()
            # print(s.before)
            # self.console_log.insert(tk.END, s.before)

            s.sendline('python vault.py')
            print("Running vault!")
            s.prompt()
            print(s.before)
            #self.console_log.insert(tk.END, s.before)

            print('Passing password to the Vault')
            s.sendline(password_text)
            s.prompt()
            # print(s.before)



            s.sendline('exit')
            s.prompt()
            print(s.before)

            print('Info shown, closing ssh')
            s.logout()

            #self.console_log.insert(tk.END, s.before)
        except pxssh.ExceptionPxssh as e:
            print("Failed SSH Authentication")
            print(e)


    def run(self):
        self.mainloop()


if __name__ == '__main__':
    app = EnergyGUI(tk.Tk())
    app.run()
