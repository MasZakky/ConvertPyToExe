import os, time, re, time
import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage

default=os.getcwd()

class GuiInfo:
    def __init__(self, text=None, title="Gui-Info"):
        self._l=0
        self.gui=tk.Tk()
        self.gui.title(title)
        self.gui.columnconfigure(0, weight=1)
        self.gui.rowconfigure(0, weight=1)
        self.gui.geometry('+0+150')
        self.frame=ttk.Frame(self.gui)
        self.frame.grid(row=0, column=0, padx=5, pady=5)
        self.gui.protocol('WM_DELETE_WINDOW', self.Quit)
        self.gui.bind('<Control-q>', self.Quit)

        if text != None:
            self.Label(text)
        self.Update()
        # self.gui.mainloop()

    def Quit(self, *arg):
        self.gui.destroy()

    def Update(self):
        self.gui.update()
        self.gui.focus()
        # pass

    def Label(self, text):
        a=ttk.Label(self.frame, text=text)
        a.grid(column=0, row=self._l, padx=5, pady=5, sticky=tk.W)
        self._l += 1

class GuiError(GuiInfo):
    def __init__(self, text=None):
        super().__init__(text, title="Internal Error")

class database:
    def __init__(self):
        self.Label_Script=None
        self.Label_Name=None
        self.Label_Logo=None

        self.Input_Script=None
        self.Input_Name=None
        self.Input_Logo=None

        self.Browse_Script=None
        self.Browse_Logo=None

        self.String_Script=None
        self.String_Name=None
        self.String_Logo=None

        self.En_Logo=False

    def Start(self, event=None):
        def Langkah(gui, text):
            gui.Label(text)
            gui.Update()

        script=self.String_Script.get().replace('/', '\\')
        script_name=script[script.rfind('\\')+1:]
        script_folder=script[:script.rfind('\\')]
        name=self.String_Name.get()
        logo=self.String_Logo.get().replace('/', '\\')
        
        if self.checkData(script, name, logo):
            GuiError('Data kurang lengkap')
            return
        
        if name.find(' ') > 0:
            self.Label_Name.configure(foreground="red")
            GuiError('Jangan ada spasi di nama')
            return

        global default
        folder=default + '\\file\\' + name
        File=['pyinstaller', '--onefile', '--windowed', 
        '--name', name]
        f_build=default +'\\build'
        f_dist=default +'\\dist'
        dist=f_dist +'\\'+ name +'.exe'
        spec=default +'\\'+ name +'.spec'

        if self.En_Logo:
            File.append('--icon='+ logo)
        File.append(script)

        gui=GuiInfo()
        gui.gui.minsize(200, 40)
        
        try:
            Langkah(gui, 'Langkah 1: convert script "{}" to exe'.format(script_name))
            os.system(' '.join(File))
            time.sleep(1)
            
            Langkah(gui, 'Langkah 2: replace files "{}.exe" to "{}"'.format(name, script_folder))
            for a in range(100):
                if "{}.exe".format(name) in os.listdir(f_dist):
                    os.system('move /y '+ dist +' '+ script_folder)
                    break
                time.sleep(0.2)
                    
            time.sleep(1)
                
            Langkah(gui, 'Langkah 3: delete files trash')
            os.system('rmdir /s /q '+ f_build)
            os.system('rmdir /s /q '+ f_dist)
            os.system('del '+ spec)
            time.sleep(1)

            Langkah(gui, 'Langkah 4: script done and open file folder')
            os.system('start '+ script_folder)
        except Exception as e:
            GuiError(e)

        time.sleep(1)
        gui.Quit()
        a=os.popen("start https://github.com/MasZakky")

    def checkData(self, script, name, logo):
        Error=False
        
        if script=="":
            Error=True
            self.Label_Script.configure(foreground="red")
        else:
            if script[-3:]=='.py':
                self.Label_Script.configure(foreground="black")
            else:
                Error=True
                self.Label_Script.configure(foreground="red")

        if name=="":
            Error=True
            self.Label_Name.configure(foreground="red")
        else:
            self.Label_Name.configure(foreground="black")

        if self.En_Logo:
            if logo=='':
                Error=True
                self.Label_Logo.configure(foreground="red")
            else:
                self.Label_Logo.configure(foreground="black")
        else:
            self.Label_Logo.configure(foreground="black")

        return Error

    def Void_Logo(self):
        if self.En_Logo:
            self.En_Logo=False
            self.Input_Logo.config(state='disabled')
            self.Browse_Logo.config(state='disabled')
        else:
            self.En_Logo=True
            self.Input_Logo.config(state='normal')
            self.Browse_Logo.config(state='normal')

    def Void_BrowseScript(self):
        nama=filedialog.askopenfilename(filetypes=(("Python (*.py)", "*.py"),
                                                     ("All files", "*.*")))
        self.Input_Script.delete(0, tk.END)
        self.Input_Script.insert(0, nama)
        self.Input_Name.delete(0, tk.END)
        if nama[-3:]=='.py':
            self.Input_Name.insert(0, nama[nama.rfind('/')+1:-3])
        else:
            self.Input_Name.insert(0, nama[nama.rfind('/')+1:])

    def Void_BrowseLogo(self):
        nama=filedialog.askopenfilename(filetypes=(("ICON (*.ico)", "*.ico"),))
        self.Input_Logo.delete(0, tk.END)
        self.Input_Logo.insert(0, nama)

class Gui:
    def __init__(self, database):
        self.database=database

        #Confiq
        self.myGUI=tk.Tk()
        self.myGUI.title('Convert File Python to File Exe')
        self.myGUI.minsize(width=700, height=50)
        self.myGUI.geometry('+0+0')
        self.myGUI.resizable(False, False)
        self.myGUI.columnconfigure(0, weight=1)
        self.myGUI.rowconfigure(0, weight=1)
        self.myGUI.iconphoto(False, PhotoImage(file='logo.png'))

        #Frame
        self.GUI=ttk.Frame(self.myGUI)
        self.GUI.grid(column=0, row=0, padx=5, pady=5)

        #ROW 0
        self.database.Label_Script=tk.Label(self.GUI, text="Script :")
        self.database.Label_Script.grid(column=0, row=0, sticky=tk.E)
        self.database.String_Script=tk.StringVar()
        self.database.Input_Script=tk.Entry(self.GUI, textvariable=self.database.String_Script, width=100)
        self.database.Input_Script.grid(column=1, row=0, columnspan=4, sticky=tk.W)
        self.database.Browse_Script=tk.Button(self.GUI, text="Browse", command=self.database.Void_BrowseScript, width=20)
        self.database.Browse_Script.grid(column=5, row=0, columnspan=1, sticky=tk.E)
        
        #ROW 1
        self.database.Label_Name=tk.Label(self.GUI, text="Name :")
        self.database.Label_Name.grid(column=0, row=1, sticky=tk.E)
        self.database.String_Name=tk.StringVar()
        self.database.Input_Name=tk.Entry(self.GUI, textvariable=self.database.String_Name, width=100)
        self.database.Input_Name.grid(column=1, row=1, columnspan=5, sticky=tk.W)
        
        #ROW 2
        self.database.Label_Logo=tk.Label(self.GUI, text="Logo :")
        self.database.Label_Logo.grid(column=0, row=2, sticky=tk.E)
        self.database.String_Logo=tk.StringVar()
        self.database.Input_Logo=tk.Entry(self.GUI, textvariable=self.database.String_Logo, width=100)
        self.database.Input_Logo.grid(column=1, row=2, columnspan=4, sticky=tk.W)
        self.database.Input_Logo.config(state='disable')
        self.database.Browse_Logo=tk.Button(self.GUI, text="Browse", command=self.database.Void_BrowseLogo, width=20)
        self.database.Browse_Logo.grid(column=5, row=2, sticky=tk.E)
        self.database.Browse_Logo.config(state='disable')
        
        #ROW 3
        checkButtonLogo=tk.Checkbutton(self.GUI, text="Enable Logo", 
                                            command=self.database.Void_Logo)
        checkButtonLogo.grid(column=0, row=3, padx=3, pady=3, sticky=tk.W)
        checkButtonLogo.deselect()
        start=tk.Button(self.GUI, text="Start", command=self.database.Start, width=20)
        start.grid(column=5, row=3, columnspan=2)
        
        #Var_Nama.bind("<Return>", self.START)
        self.database.Input_Script.bind("<Return>", self.database.Start)
        self.database.Input_Script.focus()
        self.database.Input_Name.bind("<Return>", self.database.Start)
        
        self.myGUI.protocol('WM_DELETE_WINDOW', self.Quit)
        self.myGUI.bind('<Control-q>', self.Quit)
        self.myGUI.mainloop()
       
    def Quit(self, *arg):
        self.myGUI.destroy()
    
def main():
    # def PIP_Install():
    #     gui=GuiInfo()
    #     gui.Label('Install "pyinstaller"')
    #     gui.Update()
    #     os.system('start /wait pip install pyinstaller')
    #     gui.Label('Done')
    #     time.sleep(2)
    #     gui.Quit()
    #     import PyInstaller

    # try:
    #     import PyInstaller
    # except ImportError:
    #     PIP_Install()
    # except ImportWarning:
    #     PIP_Install()
    # except Exception:
    #     PIP_Install()

    try:
        Gui(database())
    except Exception as e:
        GuiError(e)
    
if __name__=='__main__':
    main()