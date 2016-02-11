import tkinter.tix as tix
import tkinter.simpledialog

class OptionsDialog(tkinter.simpledialog.Dialog):
    def __init__(self, master, options, *args):
        self.options = options
        self.entries = []
        self.changed = False
        super().__init__(master, *args)

    def body(self, top):
        ''' define GUI elements'''
        f = tix.Frame(top)
        f.pack(expand=True, fill='x')
        for row, opt in enumerate(self.options): 
           tix.Label(f,text=opt[0]).grid(row=row, column=0, sticky='w')
           e = tix.Entry(f)
           e.grid(row=row, column=1, sticky='e')
           e.insert('end', str(opt[1]))
           self.entries.append(e)

    def apply(self):
        ''' store entry values in options '''
        for index, opt in enumerate(self.options):
            opt[1] = self.entries[index].get()
        self.changed = True

if __name__ == "__main__":
    top = tix.Tk()
    app = OptionsDialog(top,(["First","my value"],["Second","Another value"]))
    top.mainloop()
