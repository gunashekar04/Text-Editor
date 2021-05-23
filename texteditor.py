from tkinter import *
from tkinter import ttk, messagebox, font, colorchooser
from ttkthemes import ThemedTk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# setting up the GUI of the text editor
root = ThemedTk()
root.geometry("800x500+400+100")
root.title("Untitled - Text Editor")
# root.call('wm', 'iconphoto', root._w, PhotoImage(file='icons/icon.png'))     #https://www.google.com/search?q=text+editor+icon&sa=X&bih=754&biw=1536&hl=en-US&tbm=isch&source=iu&ictx=1&fir=pprhYup82Dl0vM%252C2S9THixkRtXhgM%252C_&vet=1&usg=AI4_-kRoft09CJ6qd5hgoHouqvi0lrBSzA&ved=2ahUKEwiwxJOr1dfwAhV0muYKHWQXB-MQ9QF6BAgIEAE#imgrc=pprhYup82Dl0vM
filepath = ""
noOfLines = 1
wordWrap = BooleanVar()
color_code = ["", "#000000"]
hideBar = BooleanVar()
selected_theme = StringVar()
color_theme = StringVar()


# Custom dialog to edit font
class FontDialog:

    def __init__(self, top): 
        self.top = top
        self.top.title("Fonts")
        self.top.geometry('+600+150')
        # root.call('wm', 'iconphoto', self.top._w, PhotoImage(file='icons/fonticon.png'))  # https://img.icons8.com/plumpy/2x/increase-font.png
        self.top.resizable(False, False)
        self.top.grid_rowconfigure(2, weight=1)

        self.fontText = StringVar()
        self.styleText = StringVar()
        self.sizeText = StringVar()  

        # font
        self.font_frame = ttk.Frame(top)
        self.fframe_label = ttk.Label(self.font_frame, text="Font:")
        self.fframe_entry = ttk.Entry(self.font_frame, textvariable=self.fontText) 
        self.fontText.set(textFont['family'])
        self.fframe_listframe = ttk.Frame(self.font_frame) 
        self.fframe_scrollbar = ttk.Scrollbar(self.fframe_listframe)
        self.fframe_lb = Listbox(self.fframe_listframe, width=31, height=7, bd=0, yscrollcommand=self.fframe_scrollbar.set, activestyle="none")
        self.fframe_scrollbar.config(command=self.fframe_lb.yview)

        # adding items to Listbox
        self.font_values = ['System', '8514oem', 'Fixedsys', 'Terminal', 'Modern', 'Roman', 'Script', 'Courier', 'MS Serif', 'MS Sans Serif', 'Small Fonts', 'Arial', 
        'Arabic Transparent', 'Arial Baltic', 'Arial Black', 'Bahnschrift Light', 'Bahnschrift SemiLight', 'Bahnschrift', 'Bahnschrift SemiBold', 
        'Bahnschrift Light SemiCondensed', 'Bahnschrift SemiLight SemiConde', 'Bahnschrift SemiCondensed', 'Bahnschrift SemiBold SemiConden', 'Bahnschrift Light Condensed', 
        'Bahnschrift SemiLight Condensed', 'Bahnschrift Condensed', 'Bahnschrift SemiBold Condensed', 'Calibri', 'Calibri Light', 'Cambria', 'Candara', 'Candara Light',
        'Comic Sans MS', 'Consolas', 'Constantia', 'Corbel', 'Corbel Light', 'Courier New', 'Courier New Baltic', 'Ebrima', 'Franklin Gothic Medium', 'Gadugi', 'Georgia', 
        'Impact', 'Ink Free', 'Leelawadee UI', 'Leelawadee UI Semilight', 'Lucida Console', 'Lucida Sans Unicode', 'Malgun Gothic', 'Malgun Gothic Semilight', 
        'Microsoft Himalaya', 'Microsoft JhengHei',  'Microsoft JhengHei UI', 'Microsoft JhengHei Light', 'Microsoft JhengHei UI Light', 'Microsoft New Tai Lue', 
        'Microsoft PhagsPa', 'Microsoft Sans Serif', 'Microsoft Tai Le', 'Microsoft YaHei', 'Microsoft YaHei UI', 'Microsoft YaHei Light', 'Microsoft YaHei UI Light', 
        'Microsoft Yi Baiti', 'MingLiU-ExtB', 'PMingLiU-ExtB', 'MingLiU_HKSCS-ExtB',  'Mongolian Baiti', 'MS Gothic', 'MS UI Gothic', 'MS PGothic', 'MV Boli', 'Nirmala UI', 
        'Nirmala UI Semilight', 'Palatino Linotype', 'Segoe UI', 'Segoe UI Black', 'Segoe UI Emoji', 'Segoe UI Historic', 'Segoe UI Light', 'Segoe UI Semibold', 
        'Segoe UI Semilight', 'Segoe UI Symbol', 'SimSun', 'NSimSun', 'SimSun-ExtB', 'Sitka Small', 'Sitka Text', 'Sitka Subheading', 'Sitka Heading', 'Sitka Display', 
        'Sitka Banner', 'Sylfaen', 'Symbol', 'Tahoma', 'Times New Roman', 'Times New Roman Baltic', 'Trebuchet MS', 'Verdana','Yu Gothic', 'Yu Gothic UI', 
        'Yu Gothic UI Semibold', 'Yu Gothic Light', 'Yu Gothic UI Light', 'Yu Gothic Medium', 'Yu Gothic UI Semilight', 'HP Simplified', 'HP Simplified Light', 
        'HP Simplified Jpan Light', 'HP Simplified Jpan', 'HP Simplified Hans Light', 'HP Simplified Hans', 'Ubuntu Medium']

        for f in self.font_values:
            self.fframe_lb.insert(END, f)

        self.fontText.trace('w', self.search_fontlist)  # trace calls callback function(search_fontlist here) whenever user types in Entry widget

        self.font_frame.grid(row=0, column=0, padx=10, pady=10)
        self.fframe_label.pack(anchor="w")
        self.fframe_entry.pack(anchor="w", fill=X)
        self.fframe_entry.focus_set()
        self.fframe_listframe.pack(pady=1)
        self.fframe_scrollbar.pack(side=RIGHT, fill=Y)
        self.fframe_lb.bind('<<ListboxSelect>>', self.selected_font)
        self.fframe_lb.pack()

        # font style
        self.style_frame = ttk.Frame(top)
        self.sframe_label = ttk.Label(self.style_frame, text="Font Style:")
        self.sframe_entry = ttk.Entry(self.style_frame, width=5, textvariable=self.styleText)
        self.styleText.set(textFont['weight'])
        self.sframe_listframe = ttk.Frame(self.style_frame)
        self.sframe_scrollbar = ttk.Scrollbar(self.sframe_listframe)
        self.sframe_lb = Listbox(self.sframe_listframe, width=10, height=7, bd=0, yscrollcommand=self.sframe_scrollbar.set, activestyle="none")
        self.sframe_scrollbar.config(command=self.sframe_lb.yview)

        # adding items to Listbox
        self.style_values = ['normal', 'bold', 'italic', 'roman']
        self.fontWeight = ["bold", "normal"]
        self.fontSlant = ["italic", "roman"]
        
        for style in self.style_values:
            self.sframe_lb.insert(END, style)

        self.styleText.trace('w', self.search_stylelist)  # trace calls callback function(search_stylelist here) whenever user types in Entry widget

        self.style_frame.grid(row=0, column=1, padx=10, pady=10)
        self.sframe_label.pack(anchor="w")
        self.sframe_entry.pack(anchor="w", fill=X)
        self.sframe_listframe.pack(pady=1)
        self.sframe_scrollbar.pack(side=RIGHT, fill=Y)
        self.sframe_lb.bind('<<ListboxSelect>>', self.selected_style)
        self.sframe_lb.pack()

        # size
        self.size_frame = ttk.Frame(top)
        self.zframe_label = ttk.Label(self.size_frame, text="Font Size:")
        self.zframe_entry = ttk.Entry(self.size_frame, width=2, textvariable=self.sizeText)
        self.sizeText.set(textFont['size'])
        self.zframe_listframe = ttk.Frame(self.size_frame) 
        self.zframe_scrollbar = ttk.Scrollbar(self.zframe_listframe)
        self.zframe_lb = Listbox(self.zframe_listframe, width=5, height=7, bd=0, yscrollcommand=self.zframe_scrollbar.set, activestyle="none")
        self.zframe_scrollbar.config(command=self.zframe_lb.yview)

        # adding items to Listbox
        self.size_values = [8,9,10,11,12,14,16,18,20,22,24,26,28,32,26,48,72]
        for size in self.size_values:
            self.zframe_lb.insert(END, size)

        self.sizeText.trace('w', self.search_sizelist)      # trace calls callback function(search_sizelist here) whenever user types in Entry widget 

        self.size_frame.grid(row=0, column=2, padx=10, pady=10)
        self.zframe_label.pack(anchor="w")
        self.zframe_entry.pack(anchor="w", fill=X)
        self.zframe_listframe.pack(pady=1)
        self.zframe_scrollbar.pack(side=RIGHT, fill=Y)
        self.zframe_lb.bind('<<ListboxSelect>>', self.selected_size)
        self.zframe_lb.pack()

        self.color_button = ttk.Button(self.top, text="Choose color", command=self.choose_color)
        self.color_button.grid(row=1, column= 0, padx=10, ipadx=2, sticky="w")

        # sample text
        self.sample_frame = LabelFrame(top, text="Sample Text")
        self.sampleFont = font.Font(family='Consolas', weight='normal', size=11)
        self.sample_label = ttk.Label(self.sample_frame, text="AaBb", font=self.sampleFont)

        self.sample_frame.grid(row=2, column= 0, columnspan=4, padx=10, pady=10, sticky="w")
        self.sample_label.grid(row=0, column=0, ipadx=10, ipady=10)

        # button frame
        self.button_frame = Frame(top)
        self.ok_button = ttk.Button(self.button_frame, text="OK", width=10, command=self.apply_font)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", width=10, command=top.destroy)

        self.button_frame.grid(row=3, column=1, columnspan=2, sticky="se")
        self.ok_button.pack(side=LEFT, padx=10, pady=10)
        self.cancel_button.pack(padx=5, pady=10)

        # self.top.mainloop()

    # function to search for font in the font list
    def search_fontlist(self, event, index, mode):
        self.search_font = self.fontText.get()                            
        self.index_values = list(self.fframe_lb.get(0, "end"))  # making a list of values in Listbox to get the index for a given value
        for item in self.font_values:
            if self.search_font.lower() in item.lower():
                self.fframe_lb.see(self.index_values.index(item))

    
    # function to search for font style in the font style list
    def search_stylelist(self, event, index, mode):
        self.search_style = self.styleText.get()                            
        self.index_values = list(self.sframe_lb.get(0, "end"))  # making a list of values in Listbox to get the index for a given value
        for item in self.style_values:
            if self.search_style.lower() in item.lower():
                self.sframe_lb.see(self.index_values.index(item))


    # function to search for size in font size list
    def search_sizelist(self, event, index, mode):
        self.search_size = self.sizeText.get()                            
        self.index_values = list(self.zframe_lb.get(0, "end"))  # making a list of values in Listbox to get the index for a given value
        for item in self.size_values:
            if self.search_size in str(item):
                self.zframe_lb.see(self.index_values.index(int(item)))


    def choose_color(self):
        global color_code
        color_code = colorchooser.askcolor(title="Choose color", parent=self.top)
        self.sample_label.configure(foreground=color_code[1])

            
    # function to display the selected font and apply it to sample font
    def selected_font(self, event=NONE):
        global font_selected
        for font_selected in self.fframe_lb.curselection():
            self.fontText.set(self.fframe_lb.get(font_selected))
        self.sampleFont.configure(family=self.fontText.get())


    # function to display the selected font style and apply it to sample font 
    def selected_style(self, event=NONE):
        global style_selected
        for style_selected in self.sframe_lb.curselection():
            self.styleText.set(self.sframe_lb.get(style_selected))
        if self.sframe_lb.get(style_selected) in self.fontWeight:
            self.sampleFont.configure(weight=self.styleText.get(), slant=font.ROMAN)
        else:
            self.sampleFont.configure(slant=self.sframe_lb.get(style_selected), weight=font.BOLD)


    # function to display the selected font size and apply it to sample font
    def selected_size(self, event=NONE):
        global size_selected
        for size_selected in self.zframe_lb.curselection():
            self.sizeText.set(self.zframe_lb.get(size_selected))
        self.sampleFont.configure(size=self.sizeText.get())


    # function to apply the selected font, font style, size and color to text
    def apply_font(self):
        global color_code
        if self.fontText.get() in self.font_values:
            if self.styleText.get() in self.fontWeight:      #self.sframe_lb.get(style_selected)
                textFont.configure(family=self.fontText.get(), weight=self.styleText.get(), slant=font.ROMAN, size=11 if self.sizeText.get() == "" else self.sizeText.get())
                self.top.destroy()
            elif self.styleText.get() in self.fontSlant:
                textFont.configure(family=self.fontText.get(), slant=self.styleText.get(), weight=font.BOLD, size=11 if self.sizeText.get() == "" else self.sizeText.get())
                self.top.destroy()
            else:
                messagebox.showinfo(title="Font", message="The style is not compatible with the font.\nChoose a style from the list of font styles.", parent=self.top)
        else:
            messagebox.showinfo(title="Font", message="The font is not valid.\nChoose a font from the list of fonts.", parent=self.top)

        text.config(foreground=color_code[1])

        
# Custom dialog to display themes 
class ThemeDialog:

    def __init__(self, top):
        self.top = top
        self.top.geometry('+600+150')
        self.top.resizable(False, False)
        # root.call('wm', 'iconphoto', self.top._w, PhotoImage(file='icons/themeicon.png'))     # https://img.icons8.com/pastel-glyph/2x/seo-text.png   
        self.top.title('Themes')
        self.style = ttk.Style(self.top)

        # radio button for default themes
        defaulttheme_frame = ttk.LabelFrame(self.top, text="Default Themes")
        defaulttheme_frame.grid(row=0, column=0, padx=10, pady=10, ipadx=20, ipady=20, sticky='w')
        self.default_themes = ["alt", "scidsand", "classic", "scidblue", "scidmint", "scidgreen", "scidpink", "default", "scidgrey", "scidpurple", "clam", "winnative", "xpnative", "vista"]
        for theme_name in self.default_themes:   # self.style.theme_names() returns the list of available themes(i.e., self.default_themes)
            default_rb = ttk.Radiobutton(
                defaulttheme_frame,
                text=theme_name,
                value=theme_name,
                variable=selected_theme,
                command=self.change_theme)
            default_rb.pack(expand=True, fill='both')

        # radio button for advanced themes
        advancetheme_frame = ttk.LabelFrame(self.top, text="Advance Themes")
        advancetheme_frame.grid(row=0, column=1, padx=10, pady=10, ipadx=20, ipady=20, sticky='w')
        self.advanced_themes = ["adapta", "black", "blue", "breeze", "aquativo", "clearlooks", "elegance", "equilux", "itft1", "keramik", "plastik", "radiance", "smog", "winxpblue", "yaru"]
        for theme_name in self.advanced_themes:    
            advance_rb = ttk.Radiobutton(
                advancetheme_frame,
                text=theme_name,
                value=theme_name,
                variable=selected_theme,
                command=self.change_theme)
            advance_rb.pack(expand=True, fill='both')

    
    # function to apply the selected theme
    def change_theme(self):
        self.style.theme_use(selected_theme.get())
        theme_label.config(text="Theme: " + selected_theme.get())


# Custom dialog to find a word
class FindDialog:

    def __init__(self, top):
        self.top = top
        self.top.geometry('+600+250')
        self.top.resizable(False, False)
        # root.call('wm', 'iconphoto', self.top._w, PhotoImage(file='icons/find.png'))     # https://img.icons8.com/android/2x/search.png   
        self.top.title('Find')
        self.match_case = BooleanVar()

        ttk.Label(self.top, text='Text to find:').grid(row=0, column=0, padx=10, pady=10)
        
        self.find_entry = ttk.Entry(self.top, width=25)
        self.find_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        self.find_entry.focus_set()

        self.matchCase_cb = ttk.Checkbutton(self.top, text="Match Case", onvalue=1, offvalue=0, variable=self.match_case)
        self.matchCase_cb.grid(row=1, column=0, columnspan=2, padx=10, sticky='w')

        find_btn = ttk.Button(self.top, text='Find', command=self.find)
        find_btn.grid(row=2, column=1, pady=10)

        clear_btn = ttk.Button(self.top, text='Clear', command=self.clear)
        clear_btn.grid(row=2, column=2, pady=10)


        ttk.Label(self.top, text="*String matched are marked in red color, click clear to undo color", font=("Consolas", 6), foreground="red").grid(row=3, column=0, columnspan=3)
        

    #function to search string in text
    def find(self):
        text.tag_remove('found', '1.0', END)
        find_string = self.find_entry.get()
        if find_string:
            idx = '1.0'
            while 1:
                if self.match_case.get():
                    idx = text.search(find_string, idx, nocase=0, stopindex=END)
                else:
                    idx = text.search(find_string, idx, nocase=1, stopindex=END)

                if not idx: 
                    break

                lastidx = '%s+%dc' % (idx, len(find_string))
                text.tag_add('found', idx, lastidx)
                idx = lastidx
                
            # mark found string as red
            text.tag_config('found', foreground='red')
        self.find_entry.focus_set()

    # function to clear changes from find function
    def clear(self):
        text.tag_remove('found', '1.0', END)


# Custom dialog to replace word
class ReplaceDialog:

    def __init__(self, top):
        self.top = top
        self.top.geometry('+600+250')
        self.top.resizable(False, False)
        # root.call('wm', 'iconphoto', self.top._w, PhotoImage(file='icons/replace.png'))     # https://img.icons8.com/windows/2x/find-and-replace.png  
        self.top.title('Replace')
        self.match_case = BooleanVar()
        self.match_case.set('True')

        ttk.Label(self.top, text='Text to find:').grid(row=0, column=0, padx=5, pady=10, sticky='w')
        self.find_entry = ttk.Entry(self.top, width=25)
        self.find_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
        self.find_entry.focus_set()

        ttk.Label(self.top, text='Text to replace:').grid(row=1, column=0, padx=5)
        self.replace_entry = ttk.Entry(self.top, width=25)
        self.replace_entry.grid(row=1, column=1, columnspan=2)

        self.matchCase_cb = ttk.Checkbutton(self.top, text="Match Case", onvalue=1, offvalue=0, variable=self.match_case)
        self.matchCase_cb.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky='w')

        find_btn = ttk.Button(self.top, text='Replace', command=self.replace)
        find_btn.grid(row=3, column=1, pady=10)

        clear_btn = ttk.Button(self.top, text='Cancel', command=self.top.destroy)
        clear_btn.grid(row=3, column=2, pady=10)

    # function to replace word    
    def replace(self):
        if self.find_entry.get() and self.replace_entry.get():
            find_word = self.find_entry.get()
            replace_word = self.replace_entry.get()
            text_content = text.get(1.0, END)
            if self.match_case.get():
                new_content = text_content.replace(find_word, replace_word)
            else:
                new_content = text_content.lower().replace(find_word.lower(), replace_word)
            text.delete(1.0, END)
            text.insert(1.0, new_content)
        else:
            messagebox.showinfo(title="Text Editor", message="Fields can't be empty", parent=self.top)
            self.top.destroy()
    

# function to save changes before opening a new file
def save_before_new(event=NONE):
    if text.edit_modified():
        dialog_save(1)
    else:
        new_file()


# function for new file
def new_file(event = NONE):
    global filepath
    filepath = ""
    for widget in root.winfo_children():        # to deatroy any toplevel widgets
        if isinstance(widget, Toplevel):
            widget.destroy()

    text.delete(1.0, END)
    root.title("Untitled - Text Editor")
    text.edit_modified(False)
    addr_label.config(text=" ")
    

# function to display filepath
def display():
    text.edit_modified(False)
    root.title(filepath.split("/")[-1] + " - Text Editor")
    addr_label.config(text=filepath)


# function to save changes before opening a file
def save_before_open(event=NONE):
    if text.edit_modified():
        dialog_save(2)
    else:
        open_file()


# function to open file
def open_file(event = NONE):
    global filepath
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:
        return
    text.delete(1.0, END)
    with open(filepath, "r") as input_file:
        read_text = input_file.read()
        text.insert(END, read_text)
    display()
    

# function to save new file
def save_as_file(event = NONE):
    global filepath
    filepath = asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        write_text = text.get(1.0, END)
        output_file.write(write_text)
    display()
    

# function to save changes of file
def save_file(event = NONE):
    global filepath
    if filepath:
        with open(filepath, "w") as output_file:
            write_text = text.get(1.0, END)
            output_file.write(write_text)
        text.edit_modified(False)
    else:
        save_as_file()
    if event == "exit" and filepath:
        root.destroy()
    elif event == "new" and filepath:
        new_file()
    elif event == "open" and filepath:
        open_file()


# function to create a custom dialog box to query for saving changes
def dialog_save(flag=0):
    # setting up GUI of dialog box
    top = Toplevel()
    top.title("Text Editor")
    top.geometry('350x150+600+240')
    # root.call('wm', 'iconphoto', top._w, PhotoImage(file='icons/saveicon.png'))   # https://icons8.com/icon/119003/save
    top.resizable(False,False)
    top.config(background='white')

    myFont = font.Font(family='Arial', weight='normal', size=11)

    frame = Frame(top, bg='white')
    bottomframe = Frame(top)
    if filepath:
        dialog_text = ttk.Label(frame, text="Do you want to save changes to " + filepath, background="white", foreground="#1941a0", wraplength=300, font=myFont)
    else:
        dialog_text = ttk.Label(frame, text="Do you want to save changes?", background="white", foreground="#1941a0", font=myFont)
    
    btn1 = ttk.Button(bottomframe, text="Cancel", width=8, command=top.destroy)
    if flag == 1:    # save file before opening new file
        btn2 = ttk.Button(bottomframe, text="Don't Save", width=10, command=new_file)
        btn3 = ttk.Button(bottomframe, text="Save", width=8, command=lambda: save_file("new"))
    elif flag == 2:    # save file before opening other file
        btn2 = ttk.Button(bottomframe, text="Don't Save", width=10, command=open_file)
        btn3 = ttk.Button(bottomframe, text="Save", width=8, command=lambda: save_file("open"))
    else:       # save file before exit
        btn2 = ttk.Button(bottomframe, text="Don't Save", width=10, command=root.quit)
        btn3 = ttk.Button(bottomframe, text="Save", width=8, command=lambda: save_file("exit"))

    # displaying the dialog widgets
    frame.pack(side=TOP, anchor='w')
    bottomframe.pack(side=BOTTOM, anchor='e', fill=BOTH)
    dialog_text.pack(padx=10, pady=20)
    btn1.pack(side=RIGHT, padx=8, pady=10)
    btn2.pack(side=RIGHT, padx=8, pady=10)
    btn3.pack(side=RIGHT, padx=8, pady=10)


# exit function
def exit(event = NONE):
    if text.edit_modified():
        dialog_save()
    else:
        root.destroy()


# undo function
def undo(event=NONE):
    try:
        text.edit_undo()
    except Exception as e:
        pass


# redo function
def redo(event=NONE):
    try:
        text.edit_redo()
    except Exception as e:
        pass


# toggle function to wrap words        
def wrap_word():
    if wordWrap.get():
        text.config(wrap=WORD)
        # scrollbar_horizontal.forget()
    else:
        text.config(wrap=NONE)
        # scrollbar_horizontal.pack(side=BOTTOM, fill=X)


# function to set the color theme of the text
def set_color():
    fg_color = color_theme.get()[:7]
    bg_color = color_theme.get()[8:]
    text.config(background=bg_color, foreground=fg_color)


# toggle function to hide/show status bar
# def hide_status():
#     if hideBar.get():
#         addr_frame.forget()
#     else:
#         addr_frame.pack(side=BOTTOM, fill=X)
        

# function to display the number of lines
def noOf_lines(event=NONE):
    global noOfLines
    noOfLines = list(text.get("1.0", "end")).count('\n')
    lines_label.config(text="Lines: " + str(noOfLines))


# Setting up the widgets of the text editor

# scrollbars 
scrollbar_horizontal = ttk.Scrollbar(root, orient=HORIZONTAL)
scrollbar_vertical = ttk.Scrollbar(root)

# sizegrip for resizing window
sg = ttk.Sizegrip(root)

# textarea to write and edit text
textFont = font.Font(family='Consolas', weight='normal', size=11)
text = Text(root, bd=0, yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set, wrap=NONE, font=textFont, undo=True, maxundo=-1)

# frame to display the 
addr_frame = ttk.Frame(root)
addr_label = ttk.Label(addr_frame, text=filepath)
lines_label = ttk.Label(addr_frame, text="Lines: " + str(noOfLines))
theme_label = ttk.Label(addr_frame, text="Theme: Vista")

addr_frame.pack(side=BOTTOM, fill=X)
addr_label.pack(side=LEFT, fill=X)
lines_label.pack(side=RIGHT, padx=10)
theme_label.pack(side=RIGHT, padx=10)

# connecting scrollbars to the textarea
scrollbar_vertical.config(command=text.yview)
scrollbar_horizontal.config(command=text.xview)

# displaying the widgets
scrollbar_horizontal.pack(side=BOTTOM, fill=X)
scrollbar_vertical.pack(side=RIGHT, fill=Y) 
sg.pack(in_=scrollbar_horizontal ,side=BOTTOM, anchor='se') 
text.pack(fill=BOTH, expand=TRUE)
text.focus_set()
    
     
# setting up Menu items
menubar = Menu(root)

# file menu
file = Menu(menubar, tearoff=0)
file.add_command(label="New", accelerator="Ctrl+N", command=save_before_new)
#file.add_command(label="New Window")
file.add_command(label="Open...", accelerator="Ctrl+O", command=save_before_open)
file.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
file.add_command(label="Save As...", command=save_as_file)
file.add_separator()
file.add_command(label="Exit",command=exit)
menubar.add_cascade(label="File",menu=file)

# edit menu
edit = Menu(menubar, tearoff=0)
edit.add_command(label="Undo", accelerator="Ctrl+Z", command=undo)
edit.add_command(label="Redo", accelerator="Ctrl+Y", command=redo)
edit.add_separator()
edit.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: text.event_generate("<Control-x>"))
edit.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: text.event_generate("<Control-c>"))
edit.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: text.event_generate("<Control-v>"))
edit.add_command(label="Delete", accelerator="Del", command=lambda: text.event_generate("<Delete>"))
edit.add_separator()
edit.add_command(label="Find", command= lambda: FindDialog(Toplevel()))
edit.add_command(label="Replace", command= lambda: ReplaceDialog(Toplevel()))
edit.add_separator()
edit.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: text.event_generate("<Control-a>"))
menubar.add_cascade(label="Edit", menu=edit)

# format menu
format = Menu(menubar, tearoff=0)
format.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0, variable=wordWrap, command=wrap_word, state='active')
# format.add_checkbutton(label="Hide Status Bar", onvalue=1, offvalue=0, variable=hideBar, command=hide_status, state='active')
format.add_command(label="Font", command=lambda: FontDialog(Toplevel()))
menubar.add_cascade(label="Format", menu=format)

# Themes menu
themes = Menu(menubar, tearoff=0)
themes.add_command(label="Window Themes", command=lambda: ThemeDialog(Toplevel()))
menubar.add_cascade(label="Themes", menu=themes)

# color theme submenu of Themes menu
colorThemes = Menu(themes, tearoff=0)
colorThemes.add_radiobutton(label="Light (Default)", value=('#000000','#ffffff'), variable=color_theme, command=set_color)
colorThemes.add_radiobutton(label="Light Plus", value=('#474747','#e0e0e0'), variable=color_theme, command=set_color)
colorThemes.add_radiobutton(label="Dark", value=('#c4c4c4', '#2d2d2d'), variable=color_theme, command=set_color)
themes.add_cascade(label="Color Themes", menu=colorThemes)

# help menu
help = Menu(menubar, tearoff=0)  
help.add_command(label="About")  
menubar.add_cascade(label="Help", menu=help)

root.config(menu=menubar)


# setting up shortcuts for menu items
root.bind('<Control-n>', save_before_new)
root.bind('<Control-o>', save_before_open)
root.bind('<Control-s>', save_file)
root.bind('<Control-q>', exit)
root.bind('<Control-z>', undo)
root.bind('<Control-y>', redo)


root.bind('<Return>', noOf_lines)
root.bind('<Button-1>', noOf_lines)
root.bind('<BackSpace>', noOf_lines)

root.protocol("WM_DELETE_WINDOW", exit)     # protocol to call a callback when user clicks on exit window
root.mainloop()

